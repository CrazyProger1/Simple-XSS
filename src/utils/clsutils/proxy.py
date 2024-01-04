IGNORE_FIELDS = {
    '__wrapped__'
}


class ObjectProxy:
    def __init__(self, wrapped):
        self.__wrapped__ = wrapped

    def __getattr__(self, item):
        if item == '__wrapped__':
            return self.__wrapped__

        return getattr(self.__wrapped__, item)

    def __setattr__(self, key, value):
        if key == '__wrapped__':
            return object.__setattr__(self, key, value)

        setattr(self.__wrapped__, key, value)

    def __delattr__(self, item):
        if item == '__wrapped__':
            return object.__delattr__(self, item)
        delattr(self.__wrapped__, item)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def __bool__(self):
        return bool(self.__wrapped__)

    def __getitem__(self, arg):
        return self.__wrapped__[arg]

    def __setitem__(self, arg, val):
        self.__wrapped__[arg] = val

    def __delitem__(self, arg):
        del self.__wrapped__[arg]

    def __getslice__(self, i, j):
        return self.__wrapped__[i:j]

    def __setslice__(self, i, j, val):
        self.__wrapped__[i:j] = val

    def __delslice__(self, i, j):
        del self.__wrapped__[i:j]

    def __contains__(self, ob):
        return ob in self.__wrapped__

    def __index__(self):
        return self.__wrapped__.__index__()

    def __rdivmod__(self, ob):
        return divmod(ob, self.__wrapped__)

    def __pow__(self, *args):
        return pow(self.__wrapped__, *args)

    def __ipow__(self, ob):
        self.__wrapped__ **= ob
        return self

    def __rpow__(self, ob):
        return pow(ob, self.__wrapped__)

    for name in 'repr str hash len abs complex int long float iter'.split():
        exec("def __%s__(self): return %s(self.__wrapped__)" % (name, name))

    for name in 'cmp', 'coerce', 'divmod':
        exec("def __%s__(self, ob): return %s(self.__wrapped__, ob)" % (name, name))

    for name, op in [
        ('lt', '<'), ('gt', '>'), ('le', '<='), ('ge', '>='),
        ('eq', ' == '), ('ne', '!=')
    ]:
        exec("def __%s__(self, ob): return self.__wrapped__ %s ob" % (name, op))

    for name, op in [('neg', '-'), ('pos', '+'), ('invert', '~')]:
        exec("def __%s__(self): return %s self.__wrapped__" % (name, op))

    for name, op in [
        ('or', '|'), ('and', '&'), ('xor', '^'), ('lshift', '<<'), ('rshift', '>>'),
        ('add', '+'), ('sub', '-'), ('mul', '*'), ('div', '/'), ('mod', '%'),
        ('truediv', '/'), ('floordiv', '//')
    ]:
        exec((
                 "def __%(name)s__(self, ob):\n"
                 "    return self.__wrapped__ %(op)s ob\n"
                 "\n"
                 "def __r%(name)s__(self, ob):\n"
                 "    return ob %(op)s self.__wrapped__\n"
                 "\n"
                 "def __i%(name)s__(self, ob):\n"
                 "    self.__wrapped__ %(op)s=ob\n"
                 "    return self\n"
             ) % locals())

    del name, op
