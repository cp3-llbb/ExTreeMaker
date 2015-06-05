__author__ = 'sbrochet'

class ProductManager:

    class ProductWrapper:

        def __init__(self, prefix, instance):
            self._prefix = prefix
            self._instance = instance

        def __getattr__(self, item):
            if not item.startswith(self._prefix):
                item = self._prefix + item

            return self._instance.__getattr__(item)

    def __init__(self, products):
        for product in products:
            self.__dict__[product['name']] = ProductManager.ProductWrapper(product['prefix'], product['instance'])
