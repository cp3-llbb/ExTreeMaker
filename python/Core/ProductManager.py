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

        def _get_product(self):
            """
            :return: Returns a direct reference to the product
            """
            return self._instance

    def __init__(self, tree, products):
        self._frozen = False
        self._tree = tree
        for product in products:
            self.__dict__[product['name']] = ProductManager.ProductWrapper(product['prefix'], product['instance'])

    def frozen(self):
        """ Let it go, let it go!"""
        return self._frozen

    def new_product_branch(self, product, branch_name, clazz):
        """
        Add a new branch to an already created product. This adds a new attribute to the product, and create the
        branch on the output tree
        :param product: The newly created branch will be added to this product
        :param branch_name: The new name of the branch. It'll be prefixed by the product's prefix
        :param clazz: The class of the new branch.
        :return:
        """
        if self._frozen:
            raise RuntimeError('You can\'t add a new branch to the tree if its frozen (Fill has already been '
                               'called once)')

        branch_name = product._prefix + branch_name

        instance = clazz()

        # Add the new attribute to the product
        product._get_product()[branch_name] = instance

        # Create the branch on the tree
        self._tree._create_branch(branch_name, instance)

        # Update the main tree buffer
        self._tree._buffer[branch_name] = instance

    def add_metadata(self, name, value):
        """
        Store a new metadata inside the tree UserInfo
        :param name: Name of the new object added to the UserInfo list
        :param value: The value to store into the UserList list
        :return: Nothing
        """

        data = None
        if isinstance(value, str):
            from ROOT import TNamed
            data = TNamed()
            data.SetTitle(value)

        if data is None:
            raise TypeError('Unsupported metadata type: %r' % value.__class__.__name__)

        data.SetName(name)
        self._tree.GetUserInfo().Add(data)