class Validator(object):
    error = None

    def get_error(self):
        if callable(self.error):
            result = self.error()
        else:
            result = self.error

        return result

    def __call__(self, form, field):
        raise NotImplementedError()
