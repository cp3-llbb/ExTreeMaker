__author__ = 'sbrochet'

from Core.Runnable import Runnable

from pytree import TreeModel, BoolCol

class Cut(object):
    class Model(TreeModel):
        cut = BoolCol(default=False)

    def __init__(self, name, description='', cut=None):
        self.name = name
        self.description = description
        self.cut = None
        if cut is not None:
            # Compile the cut for a faster evaluation
            self.cut = compile(cut, '<cut:%s>' % name, 'eval')
        self.model = Cut.Model.prefix(name + '_')()

    def evaluate(self, products):
        """
        Evaluate this cut.
        :return:
        """
        if self.cut is None:
            return

        setattr(self.model, self.name + '_cut', eval(self.cut, products.__dict__))

    def pass_cut(self):
        if self.cut is not None:
            return

        setattr(self.model, self.name + '_cut', True)

    def status(self):
        return getattr(self.model, self.name + '_cut')

class Category(object):
    class Model(TreeModel):
        category = BoolCol(default=False)

    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.model = Category.Model.prefix(name + "_")()
        self.cuts = {}
        self.in_category = False

    def _test_event_category(self, products):
        self.in_category = self.event_in_category(products)
        setattr(self.model, self.name + '_category', self.in_category)

        return self.in_category

    def reset(self):
        self.model.reset()
        self.in_category = False

    def event_in_category(self, products):
        """
        Test if the current event is in this category
        :param products: The products produced for this event
        :return: True if the current event is in this category, False otherwise
        """
        raise NotImplementedError('You must implement the event_in_category method')

    def register_cuts(self):
        pass

    def _evaluate_cuts(self, products):
        """
        Private method. Iterate over all cuts and evaluate automatically those which have a cut string
        :param products:
        :return:
        """
        for cut in self.cuts.itervalues():
            cut.evaluate(products)

        self.evaluate_cuts(products)

    def evaluate_cuts(self, products):
        pass

    def new_cut(self, name, description='', cut=None):
        """
        Register a new cut
        :param name: The name of the cut
        :param description: A description of the cut
        :return: Nothing
        """
        if ':' in name:
            raise NameError('Invalid character in cut name: \':\'')

        self.cuts[name] = Cut(self.name + '_' + name, description, cut)

    def pass_cut(self, name):
        """
        Set the status of the cut ``name`` to True
        :param name: The name of the cut
        :return:
        """

        if name not in self.cuts:
            raise KeyError('The cut %r is not registered. Please call \'new_cut\' from __init__ first.' % name)

        self.cuts[name].pass_cut()

class Analyzer(Runnable):
    """The base class of all user-defined analyzers"""

    def __init__(self, **kwargs):
        Runnable.__init__(self)

        self._categories = {}

    def analyze(self, event, products):
        """
        Main function of the analyzer. Called for each event.
        :param event: The current event
        :param products: an instance of :class:`Core.ProductManager``. You can access from it all the products produced
                by others producers
        :return:
        """
        raise NotImplementedError()

    def new_category(self, category):
        """
        Register a new category.
        :param category: An instance of a class deriving from :class:``Category``
        :return: Nothing
        """
        if not issubclass(category.__class__, Category):
            raise TypeError('`category` must be an instance of a subclass of Category')

        self._categories[category.name] = category
