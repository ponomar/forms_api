from forms_api.validators.base_validator import Validator


class NumberRangeValidator(Validator):
    def __init__(self, min=None, max=None, error=None):
        """
        :param min: 
        :param max: 
        :param error: leave None to use redefined in get_error_(min/max/min_max)
        """
        if min is None and max is None:
            raise ValueError('`min` or `max` must be specified')
        elif min is not None and max is not None and min >= max:
            raise ValueError('`min` must be less than `max`')

        self.min = min
        self.max = max
        self.error = error

    @staticmethod
    def get_error_min(min):
        return 'Must be not less than %d.' % min

    @staticmethod
    def get_error_max(max):
        return 'Must be not greater than %d.' % max

    @staticmethod
    def get_error_min_max(min, max):
        return 'Must be between %d and %d.' % (min, max)

    def get_error(self):
        error = super().get_error()
        if error is None:
            if self.min is not None and self.max is not None:
                error = self.get_error_min_max(self.min, self.max)
            elif self.min is not None:
                error = self.get_error_min(self.min)
            else:
                error = self.get_error_max(self.max)

        return error

    def schema(self):
        result = dict(type='number', rule='range', error=self.get_error())
        if self.min is not None:
            result['min'] = self.min
        if self.max:
            result['max'] = self.max

        return result

    def __call__(self, form, field):
        if field.value is None:
            return

        if self.min is not None and self.max is not None:
            if field.value < self.min or field.value > self.max:
                return self.get_error()
        elif self.min is not None:
            if field.value < self.min:
                return self.get_error()
        else:
            if field.value > self.max:
                return self.get_error()
