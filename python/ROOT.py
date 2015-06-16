from __future__ import generators
# @(#)root/pyroot:$Id$
# Author: Wim Lavrijsen (WLavrijsen@lbl.gov)
# Created: 02/20/03
# Last: 06/29/14

"""PyROOT user module.

 o) install lazy ROOT class/variable lookup as appropriate
 o) feed gSystem and gInterpreter for display updates
 o) add readline completion (if supported by python build)
 o) enable some ROOT/Cling style commands
 o) handle a few special cases such as gPad, STL, etc.
 o) execute rootlogon.py/.C scripts

"""

__version__ = '7.0.0'
__author__  = 'Wim Lavrijsen (WLavrijsen@lbl.gov)'


### system and interpreter setup ------------------------------------------------
import sys, types

### load PyROOT C++ extension module, special case for linux and Sun ------------
needsGlobal =  ( 0 <= sys.platform.find( 'linux' ) ) or\
               ( 0 <= sys.platform.find( 'sunos' ) )
if needsGlobal:
 # change dl flags to load dictionaries from pre-linked .so's
   dlflags = sys.getdlopenflags()
   sys.setdlopenflags( 0x100 | 0x2 )    # RTLD_GLOBAL | RTLD_NOW

import libPyROOT as _root

# reset dl flags if needed
if needsGlobal:
   sys.setdlopenflags( dlflags )
del needsGlobal

## convince inspect that PyROOT method proxies are possible drop-ins for python
## methods and classes for pydoc
import inspect

inspect._old_isfunction = inspect.isfunction
def isfunction( object ):
   if type(object) == _root.MethodProxy and not object.im_class:
      return True
   return inspect._old_isfunction( object )
inspect.isfunction = isfunction

inspect._old_ismethod = inspect.ismethod
def ismethod( object ):
   if type(object) == _root.MethodProxy:
      return True
   return inspect._old_ismethod( object )
inspect.ismethod = ismethod

del isfunction, ismethod


### configuration ---------------------------------------------------------------
class _Configuration( object ):
   __slots__ = [ 'IgnoreCommandLineOptions', 'StartGuiThread', 'ExposeCppMacros', '_gts' ]

   def __init__( self ):
      self.IgnoreCommandLineOptions = 0
      self.StartGuiThread = True
      self.ExposeCppMacros = False
      self._gts = []

   def __setGTS( self, value ):
      for c in value:
         if not callable( c ):
            raise ValueError( '"%s" is not callable' % str(c) );
      self._gts = value

   def __getGTS( self ):
      return self._gts

   GUIThreadScheduleOnce = property( __getGTS, __setGTS )

PyConfig = _Configuration()
del _Configuration


### choose interactive-favored policies -----------------------------------------
_root.SetMemoryPolicy( _root.kMemoryHeuristics )
_root.SetSignalPolicy( _root.kSignalSafe )


### data ________________________________________________________________________
__pseudo__all__ = [ 'gROOT', 'gSystem', 'gInterpreter',
                    'AddressOf', 'MakeNullPointer', 'Template', 'std' ]
__all__         = []                         # purposedly empty

_orig_ehook = sys.excepthook

## for setting memory and speed policies; not exported
_memPolicyAPI = [ 'SetMemoryPolicy', 'SetOwnership', 'kMemoryHeuristics', 'kMemoryStrict' ]
_sigPolicyAPI = [ 'SetSignalPolicy', 'kSignalFast', 'kSignalSafe' ]


### helpers ---------------------------------------------------------------------
def split( str ):
   npos = str.find( ' ' )
   if 0 <= npos:
      return str[:npos], str[npos+1:]
   else:
      return str, ''


### template support ------------------------------------------------------------
class Template:
   def __init__( self, name ):
      self.__name__ = name

   def __call__( self, *args ):
      newargs = [ self.__name__[ 0 <= self.__name__.find( 'std::' ) and 5 or 0:] ]
      for arg in args:
         if type(arg) == str:
            arg = ','.join( map( lambda x: x.strip(), arg.split(',') ) )
         newargs.append( arg )
      result = _root.MakeRootTemplateClass( *newargs )

    # XX: Code commented. It's called very often and is a real bottleneck
    # special case pythonization (builtin_map is not available from the C-API)
    #   if hasattr( result, 'push_back' ):
    #      def iadd( self, ll ):
    #         [ self.push_back(x) for x in ll ]
    #         return self
    #
    #      result.__iadd__ = iadd

      return result

_root.Template = Template


### scope place holder for STL classes ------------------------------------------
class _stdmeta( type ):
   def __getattr__( cls, attr ):   # for non-templated classes in std
      klass = _root.MakeRootClass( attr, cls )
      setattr( cls, attr, klass )
      return klass

class std( object ):
   __metaclass__ = _stdmeta

   stlclasses = ( 'complex', 'pair', \
      'deque', 'list', 'queue', 'stack', 'vector', 'map', 'multimap', 'set', 'multiset' )

   for name in stlclasses:
      locals()[ name ] = Template( "std::%s" % name )

   string = _root.MakeRootClass( 'string' )

_root.std = std
sys.modules['ROOT.std'] = std


### special cases for gPad, gVirtualX (are C++ macro's) -------------------------
class _ExpandMacroFunction( object ):
   def __init__( self, klass, func ):
      c = _root.MakeRootClass( klass )
      self.func = getattr( c, func )

   def __getattr__( self, what ):
      return getattr( self.__dict__[ 'func' ](), what )

   def __cmp__( self, other ):
      return cmp( self.func(), other )

   def __nonzero__( self ):
      if self.func():
         return True
      return False

   def __repr__( self ):
      return repr( self.func() )

   def __str__( self ):
      return str( self.func() )

_root.gPad         = _ExpandMacroFunction( "TVirtualPad",  "Pad" )
_root.gVirtualX    = _ExpandMacroFunction( "TVirtualX",    "Instance" )
_root.gDirectory   = _ExpandMacroFunction( "TDirectory",   "CurrentDirectory" )
_root.gFile        = _ExpandMacroFunction( "TFile",        "CurrentFile" )
_root.gInterpreter = _ExpandMacroFunction( "TInterpreter", "Instance" )


### special case pythonization --------------------------------------------------
def _TTree__iter__( self ):
   i = 0
   bytes_read = self.GetEntry(i)
   while 0 < bytes_read:
      yield self                   # TODO: not sure how to do this w/ C-API ...
      i += 1
      bytes_read = self.GetEntry(i)

   if bytes_read == -1:
      raise RuntimeError( "TTree I/O error" )

_root.MakeRootClass( "TTree" ).__iter__    = _TTree__iter__


### set import hook to be able to trigger auto-loading as appropriate
import __builtin__
_orig_ihook = __builtin__.__import__
def _importhook( name, glbls = {}, lcls = {}, fromlist = [], level = -1 ):
   if name[0:5] == 'ROOT.':
      try:
         sys.modules[ name ] = getattr( sys.modules[ 'ROOT' ], name[5:] )
      except Exception:
         pass
   if 5 <= sys.version_info[1]:    # minor
      return _orig_ihook( name, glbls, lcls, fromlist, level )
   return _orig_ihook( name, glbls, lcls, fromlist )

__builtin__.__import__ = _importhook


### allow loading ROOT classes as attributes ------------------------------------
class ModuleFacade( types.ModuleType ):
   def __init__( self, module ):
      types.ModuleType.__init__( self, 'ROOT' )

      self.__dict__[ 'module' ]   = module

      self.__dict__[ '__doc__'  ] = self.module.__doc__
      self.__dict__[ '__name__' ] = self.module.__name__
      self.__dict__[ '__file__' ] = self.module.__file__

      self.__dict__[ 'keeppolling' ] = 0
      self.__dict__[ 'PyConfig' ]    = self.module.PyConfig

    # begin with startup gettattr/setattr
    #   self.__class__.__setattr__ = self.__class__.__setattr1
    #   del self.__class__.__setattr1

   # def __setattr1( self, name, value ):      # "start-up" setattr
   #  # create application, thread etc.
   #    self.__finalSetup()
   #    del self.__class__.__finalSetup
   #
   #  # let "running" setattr handle setting
   #    return setattr( self, name, value )

   def __setattr__( self, name, value ):     # "running" getattr
    # to allow assignments to ROOT globals such as ROOT.gDebug
      if not name in self.__dict__:
         try:
          # assignment to an existing ROOT global (establishes proxy)
            setattr( self.__class__, name, _root.GetRootGlobal( name ) )
         except LookupError:
          # allow a few limited cases where new globals can be set
            if sys.hexversion >= 0x3000000:
               pylong = int
            else:
               pylong = long
            tcnv = { bool        : 'bool %s = %d;',
                     int         : 'int %s = %d;',
                     pylong      : 'long %s = %d;',
                     float       : 'double %s = %f;',
                     str         : 'string %s = "%s";' }
            try:
               _root.gROOT.ProcessLine( tcnv[ type(value) ] % (name,value) );
               setattr( self.__class__, name, _root.GetRootGlobal( name ) )
            except KeyError:
               pass           # can still assign normally, to the module

    # actual assignment through descriptor, or normal python way
      return super( self.__class__, self ).__setattr__( name, value )

   def __getattr__( self, name ):             # "running" getattr
        # lookup into ROOT (which may cause python-side enum/class/global creation)
      attr = _root.LookupRootEntity( name, PyConfig.ExposeCppMacros )

    # the call above will raise AttributeError as necessary; so if we get here,
    # attr is valid: cache as appropriate, so we don't come back
      if type(attr) == _root.PropertyProxy:
         setattr( self.__class__, name, attr )         # descriptor
         return getattr( self, name )
      else:
         self.__dict__[ name ] = attr                  # normal member
         return attr

    # reaching this point means failure ...
      raise AttributeError( name )

   def __delattr__( self, name ):
    # this is for convenience, as typically lookup results are kept at two places
      try:
         delattr( self.module._root, name )
      except AttributeError:
         pass

      return super( self.__class__, self ).__delattr__( name )

sys.modules[ __name__ ] = ModuleFacade( sys.modules[ __name__ ] )
del ModuleFacade


### b/c of circular references, the facade needs explicit cleanup ---------------
import atexit
def cleanup():

 # restore hooks
   import sys
   __builtin__.__import__ = _orig_ihook

   facade = sys.modules[ __name__ ]

 # prevent further spurious lookups into ROOT libraries
   del facade.__class__.__getattr__
   del facade.__class__.__setattr__

 # remove otherwise (potentially) circular references
   import types
   items = facade.module.__dict__.items()
   for k, v in items:
      if type(v) == types.ModuleType:
         facade.module.__dict__[ k ] = None
   del v, k, items, types

 # destroy facade
   facade.__dict__.clear()
   del facade

 # run part the gROOT shutdown sequence ... running it here ensures that
 # it is done before any ROOT libraries are off-loaded, with unspecified
 # order of static object destruction; 
   gROOT = sys.modules[ 'libPyROOT' ].gROOT
   gROOT.EndOfProcessCleanups()
   del gROOT

 # cleanup cached python strings
   sys.modules[ 'libPyROOT' ]._DestroyPyStrings()

 # destroy ROOT extension module and ROOT module
   del sys.modules[ 'libPyROOT' ]
   del sys.modules[ 'ROOT' ]

atexit.register( cleanup )
del cleanup, atexit

