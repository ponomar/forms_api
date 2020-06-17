from decimal import Decimal

from forms_api.fields.base_field import Field


ERROR_NOT_VALID_FLOAT = 'Not valid float.'


def coerce_float(value):
    if value is None or value == '':
        return
    elif isinstance(value, (str, int, Decimal)):
        return float(value)
    else:
        return value


class FloatField(Field):
    type = 'float'
    input_type = 'number'

    def __init__(self, key=None, label=None, validators=None, default=None,
                 coerce=coerce_float, required=False, required_error=None,
                 params=None, not_valid_error=ERROR_NOT_VALID_FLOAT, ndigits=None):
        super().__init__(
            key=key,
            label=label,
            validators=validators,
            default=default,
            required=required,
            required_error=required_error,
            not_valid_error=not_valid_error,
            params=params,
            coerce=coerce,
        )
        self.ndigits = ndigits

    @property
    def value(self):
        value = super().value
        if value is not None and self.ndigits is not None:
            value = round(value, ndigits=self.ndigits)
        return value
