from DataFormats.FWLite import Events, Handle
from datetime import datetime
from collections import Iterable, namedtuple
from types import StringTypes


class AnalysisEvent(Events):
    """A class that complements fwlite::Events with analysis facilities.
       The class provides the following additional functionality:
         1. instrumentation for event weight
              A set of weight classes can be defined, and the event weight
              is computed and cached using those.
         2. list of event products used in the analysis
              It allows to ask later on simply for "jets" or "electrons"
              to run the fwlite::Handle machinery and/or get the cached result.
         3. a list of "producers" of analysis high-level quantities
              It allows to run "analysis on demand", by automatically running
              the defined producers to fill the cache, and later use that one.
         4. a volatile dictionary
              It allows to use the event as an heterogeneous container for
              any analysis product. The event is properly reset when iterating
              to the next event.
    """

    Alias = namedtuple("Alias", "to")

    def __init__(self, input_files):
        """
        Main constructor
        :param input_files: Either a list of input files or a single file name
        :return: Nothing
        """
        Events.__init__(self, input_files)

        # additional features:
        # a list of event products used in the analysis
        self._collections = {}

        # volatile dictionary. User can add any quantity to the event and it will be
        #    properly erased in the iteration step.

        self.__dict__["vardict"] = {}

    def addCollection(self, name, handle, inputTag):
        """Register an event collection as used by the analysis.
           Example: addCollection("jets","vector<pat::Jet>","cleanPatJets" """
        if name in self._collections:
            # Check if handle and inputTag is different before throwing
            oldC = self._collections[name]
            if oldC['handle']._type.strip() != handle.strip() or oldC['collection'].strip() != inputTag.strip():
                raise KeyError("%r collection is already declared as %s:%s" % (name, oldC['handle']._type, oldC['collection']))
            else:
                # Collection already exists
                return

        if hasattr(self, name):
            raise AttributeError("%r object already has attribute %r" % (type(self).__name__, name))

        # Look if there's already a collection registered for this handle and inputTag. If there is, consider this
        # collection as an alias of the other
        for collectionName, collectionData in self._collections.items():
            if handle.strip() == collectionData['handle']._type.strip() and \
                    inputTag.strip() == collectionData['collection'].strip():
                print("Collection %r set as an alias of collection %r" % (name, collectionName))
                self._collections[name] = AnalysisEvent.Alias(to=collectionName)
                return

        self._collections[name] = {"handle": Handle(handle), "collection": inputTag}

    def removeCollection(self, name):
        """Forget about the named event collection.
           This method will delete both the product from the cache (if any) and the definition.
           To simply clear the cache, use "del event.name" instead. """
        del self._collections[name]
        if name in self.vardict:
            delattr(self, name)

    def run(self):
        """Run number"""
        return self.eventAuxiliary().run()

    def event(self):
        """Event number"""
        return self.eventAuxiliary().id().event()

    def lumi(self):
        """Lumisection"""
        return self.eventAuxiliary().luminosityBlock()

    def to(self, run, event, lumi=None):
        """Jump to some event,run,lumisection"""
        if self._veryFirstTime:
            self._createFWLiteEvent()
        if lumi is None:
            return self._event.to(long(run), long(event))
        else:
            return self._event.to(long(run), long(lumi), long(event))

    def __getitem__(self, index):
        """Jump to some event,run,(lumisection) or to a given event index"""
        if len(index) == 3:
            self.to(index[0], index[1], index[2])
        elif len(index) == 2:
            self.to(index[0], index[1])
        elif len(index) == 1:
            self.to(index[0])
        else:
            raise TypeError("Events must be indexed by run, event, (lumi) or by event index.")
        return self

    def _next(self):
        """(Internal) Iterator internals"""
        # I was willing to call the super._next() with some additional stuff but I didn't find a way.
        # So, I just duplicate the code with some modifications.
        if self._veryFirstTime:
            self._createFWLiteEvent()
        if self._toBegin:
            self._toBeginCode()
        while not self._event.atEnd():
            self.vardict.clear()  # added
            yield self
            self._eventCounts += 1
            if 0 < self._maxEvents <= self._eventCounts:
                break
            # Have we been asked to go to the first event?
            if self._toBegin:
                self._toBeginCode()
            else:
                # if not, lets go to the next event
                self._event.__preinc__()

    def __getattr__(self, attr):
        """Overloaded getter to handle properly:
             - volatile analysis objects
             - event collections
             - data producers"""
        if attr in self.__dict__["vardict"]:
            return self.vardict[attr]
        if attr in self._collections:
            obj = self._collections[attr]
            if isinstance(obj, AnalysisEvent.Alias):
                return self.__getattr__(obj.to)

            try:
                self.getByLabel(obj["collection"], obj["handle"])
                return self.vardict.setdefault(attr, obj["handle"].product())
            except:
                return self.vardict.setdefault(attr, None)

        raise AttributeError("%r object has no attribute %r" % (type(self).__name__, attr))

    def __setattr__(self, name, value):
        """Overloaded setter that puts any new attribute in the volatile dict."""
        if name in self.__dict__ or not "vardict" in self.__dict__ or name[0] == '_':
            self.__dict__[name] = value
        else:
            if name in self._collections:
                raise AttributeError(
                    "%r object %r attribute is read-only (event collection)" % (type(self).__name__, name))
            self.vardict[name] = value

    def __delattr__(self, name):
        """Overloaded del method to handle the volatile internal dictionary."""
        if name == "vardict":
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, name))
        if name in self.__dict__:
            del self.__dict__[name]
        elif name in self.vardict:
            del self.vardict[name]
        else:
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, name))

    def _dicthash(self, dict):
        return (lambda d, j='=', s=';': s.join([j.join((str(k), str(v))) for k, v in d.iteritems()]))(dict)

    def __str__(self):
        """Event text dump."""
        dictjoin = lambda d, j=' => ', s='\n': s.join([j.join((str(k), str(v))) for k, v in d.iteritems()])
        mystring = "=================================================================\n"
        # general information
        mystring += "Run %d - Lumisection %d, Event %d\n" % (self.eventAuxiliary().run(),
                                                             self.eventAuxiliary().luminosityBlock(),
                                                             self.eventAuxiliary().id().event())
        mystring += "Recorded on %s\n" % datetime.fromtimestamp(self.eventAuxiliary().time().unixTime()).strftime(
            "%Y-%m-%d %H:%M:%S")
        mystring += "-----------------------------------------------------------------\n"
        # list the collections
        mystring += "Collections:\n"
        for colname in self._collections.keys():
            collection = self.getCollection(colname)
            if mystring[-1] != '\n': mystring += '\n'
            try:
                if isinstance(collection[0], float):  # protection... DoubleBuffer is seen with a large size
                    mystring += "*** %s is a float whose value is %f\n" % (colname, collection[0])
                else:
                    mystring += "*** %s has %d elements\n" % (colname, len(collection))
                    mystring += reduce(lambda a, b: a + b, map(str, collection), "")
            except IndexError:
                mystring += "*** %s has %d elements\n" % (colname, len(collection))
            except TypeError:
                if collection is not None:
                    mystring += "*** %s has 1 element\n" % colname
                    mystring += str(collection)
            except:
                pass
        mystring += "\n-----------------------------------------------------------------\n"

        # list the content of vardict, excluding collections
        mystring += "Content of the cache:\n"
        for k, v in self.vardict.iteritems():
            if k in self._collections.keys(): continue
            if isinstance(v, Iterable) and not isinstance(v, StringTypes):
                try:
                    thisstring = "%s => vector of %d objects(s)\n" % (k, len(v))
                except:
                    mystring += "%s => %s\n" % (k, str(v))
                else:
                    try:
                        for it, vec in enumerate(v):
                            thisstring += "%s[%d] = %s\n" % (k, it, str(vec))
                    except:
                        mystring += "%s => %s\n" % (k, str(v))
                    else:
                        mystring += thisstring
            else:
                mystring += "%s => %s\n" % (k, str(v))
        return mystring
