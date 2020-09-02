import weakref


class _BaseCallable():
    def __init__(self, f):
        self._function = f

    def is_alive(self):
        return self._function is not None and self._function() is not None

    def call(self, *a, **kw):
        raise NotImplementedError


class _FunctionCallable(_BaseCallable):
    def call(self, *a, **kw):
        self._function()(*a, **kw)


class _MethodCallable(_BaseCallable):
    def __init__(self, f, t):
        _BaseCallable.__init__(self, f)

        self._target = t

    def call(self, *a, **kw):
        # TODO
        # self._function()(self._target, *a, **kw)
        self._function()(self._target(), *a, **kw)


class ConnectEmit():
    _SUPPORTED_KEYWORDS = ['arguments']

    def __init__(self, *args, **kwargs):
        self._types = []
        self._keywords = []

        self._callables = {}

        for a in args:
            if type(a) is not type:
                raise TypeError("Type '%s' not valid!" % a)

            self._types.append(a.__name__)

        for k in kwargs:
            if k not in self._SUPPORTED_KEYWORDS:
                raise TypeError("Keyword '%s' not supported!", k)
            elif k == 'arguments':
                self._keywords = kwargs[k]

    def _cleanup(self, ref):
        del self._callables[id(ref)]

    def connect(self, f):
        if type(f).__name__ not in ['function', 'method']:
            raise TypeError("'%s' is not a function or instance method" %
                            type(f).__name__)

        # XXX weakref.WeakMethod on python3
        if type(f).__name__ == 'method':
            ref = weakref.ref(f.__func__)
            ref_self = weakref.ref(f.__self__, self._cleanup)

            # TODO
            self._callables[id(ref_self)] = _MethodCallable(ref, ref_self)
            # self._callables[id(ref)] = _MethodCallable(ref, ref_self)
        else:
            ref = weakref.ref(f, self._cleanup)
            self._callables[id(ref)] = _FunctionCallable(ref)

    def disconnect(self, f):
        pass
        # TODO
        # del self._callables[id(weakref.ref(f))]

    def emit(self, *args, **kwargs):
        if not self._callables:
            return

        for i, arg in enumerate(args):
            t = type(arg).__name__
            if t != self._types[i]:
                raise TypeError("Wrong argument type: '%s' (expected: %s, "
                                "received: %s)" % (arg, self._types[i], t))

        keywords = {}
        len_keywords = len(self._keywords)
        if len_keywords > 0:
            len_args = len(args)
            if len_keywords != len_args:
                raise TypeError("Wrong number of arguments (expected: %s, "
                                "received: %s)" % (len_keywords, len_args))

            for i, k in enumerate(self._keywords):
                keywords[k] = args[i]

        for c in self._callables.values():
            if not c.is_alive():
                continue

            if keywords:
                c.call(**keywords)
            else:
                c.call(*args, **kwargs)
