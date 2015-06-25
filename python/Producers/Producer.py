__author__ = 'sbrochet'

import math

from Core.Runnable import Runnable

class Cutable(object):

    math_locals = {v: getattr(math, v) for v in filter(lambda x: not x.startswith('_'), dir(math))}

    def __init__(self, name, cut):
        self.cut = None
        if cut is not None:
            # Compile the cut for a faster evaluation
            self.cut = compile(cut, '<cut:%s>' % name, 'eval')

    def pass_cut(self, obj):
        if self.cut is None:
            return True
        l = dict(Cutable.math_locals, **Cutable._get_locals(obj))
        return eval(self.cut, {}, l)

    @staticmethod
    def _get_locals(obj):
        return {v: getattr(obj, v) for v in filter(lambda x: not x.startswith('_'), dir(obj))}


class Producer(Runnable, Cutable):

    def __init__(self, name, **kwargs):
        Runnable.__init__(self)
        Cutable.__init__(self, name, kwargs['cut'] if 'cut' in kwargs else None)

        self._name = name

    def produce(self, event, products):
        raise NotImplementedError()