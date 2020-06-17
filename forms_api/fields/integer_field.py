from forms_api.fields.base_field import Field


ERROR_NOT_VALID_INTEGER = 'Not valid integer.'


def coerce_int(value):
    if value is None or value == '':
        return
    elif isinstance(value, str):
        return int(value)
    elif not isinstance(value, int):
        raise ValueError

    return value


class IntegerField(Field):
    type = 'integer'
    input_type = 'number'

    def __init__(self, key=None, label=None, validators=None, default=None,
                 coerce=coerce_int, required=False, required_error=None,
                 params=None, not_valid_error=ERROR_NOT_VALID_INTEGER):
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
