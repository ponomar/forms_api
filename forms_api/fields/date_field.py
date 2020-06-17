from datetime import datetime, date

from forms_api.fields.base_field import Field


ERROR_NOT_VALID_DATE = 'Not valid date.'


def coerce_date(value):
    if value is None or value == '':
        return
    elif isinstance(value, str):
        return datetime.strptime(value, '%Y-%m-%d').date()
    elif not isinstance(value, date) or isinstance(value, datetime):
        raise ValueError

    return value


class DateField(Field):
    type = 'date'
    input_type = 'date'

    def __init__(self, key=None, label=None, validators=None, default=None,
                 coerce=coerce_date, required=False, required_error=None,
                 params=None, not_valid_error=ERROR_NOT_VALID_DATE):
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

    @property
    def value_schema(self):
        result = self.value
        if isinstance(result, date):
            result = str(result)
        return result
