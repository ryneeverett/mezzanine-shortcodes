class classproperty(object):
    """ From http://stackoverflow.com/a/5192374/1938621. """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
