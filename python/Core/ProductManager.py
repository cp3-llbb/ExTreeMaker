__author__ = 'sbrochet'

class ProductManager:

    class ProductWrapper:

        def __init__(self, prefix, instance):
            # Use __dict__ to avoid a call to __setattr__
            self.__dict__['_prefix'] = prefix
            self.__dict__['_instance'] = instance

        def __getattr__(self, item):
            if not item.startswith(self._prefix):
                item = self._prefix + item

            return self._instance.__getattr__(item)

        def __setattr__(self, item, value):
            if not item.startswith(self._prefix):
                item = self._prefix + item

            return self._instance.__setattr__(item, value)

    def __init__(self, products):
        for product in products:
            self.__dict__[product['name']] = ProductManager.ProductWrapper(product['prefix'], product['instance'])
