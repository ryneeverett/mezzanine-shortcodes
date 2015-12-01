class classproperty(object):
    """ Posted to http://stackoverflow.com/a/32289080/1938621. """
    def __init__(self, f):
        self.f = f

    def __get__(self, instance, klass):
        if instance:
            try:
                return self.f(instance)
            except AttributeError:
                pass
        return self.f(klass)
