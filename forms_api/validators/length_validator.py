from forms_api.validators.base_validator import Validator


class LengthValidator(Validator):
    def __init__(self, min=None, max=None, error=None, error_count=None):
        """
        :param min: 
        :param max: 
        :param error: leave None to use redefined in get_error_(min/max/min_max)
        :param error_count: leave None to use redefined in get_error_count
        """

        if min is None and max is None:
            raise ValueError('`min` or `max` must be specified')
        elif min is not None and max is not None and min >= max:
            raise ValueError('`min` must be less than `max`')
        elif min is not None and min < 0:
            raise ValueError('`min` can not be less than 0')
        elif max is not None and max < 1:
            raise ValueError('`max` can not be less than 1')

        self.min = min
        self.max = max
        self.error = error
        self.error_count = error_count  # "You've typed %d symbols."

    @staticmethod
    def get_error_min(min):
        return 'Must be from %d symbols.' % min

    @staticmethod
    def get_error_max(max):
        return 'Must be up to %d symbols.' % max

    @staticmethod
    def get_error_min_max(min, max):
        return 'Must be from %d to %d symbols.' % (min, max)

    @staticmethod
    def get_error_count():
        return 'You\'ve typed %s symbols.'

    def get_error(self, count=None):
        error = super().get_error()
        if error is None:
            if self.min is not None and self.max is not None:
                error = self.get_error_min_max(self.min, self.max)
            elif self.min is not None:
                error = self.get_error_min(self.min)
            else:
                error = self.get_error_max(self.max)

        if count is not None:
            error_count = self.error_count
            if error_count is None:
                error_count = self.get_error_count()
            if error_count:
                if callable(error_count):
                    error_count = error_count()

                error = '%s %s' % (error, error_count % count)

        return error

    def schema(self):
        result = dict(type='string', rule='length', error=self.get_error())
        if self.min is not None:
            result['min'] = self.min
        if self.max is not None:
            result['max'] = self.max

        return result

    def __call__(self, form, field):
        count = len(field.value or '')
        if count == 0 and field.required is False:
            return

        if self.min is not None and self.max is not None:
            if count < self.min or count > self.max:
                return self.get_error(count)
        elif self.min is not None:
            if count < self.min:
                return self.get_error(count)
        else:
            if count > self.max:
                return self.get_error(count)
