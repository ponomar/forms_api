from forms_api.fields.base_field import Field


class StringField(Field):
    type = 'string'
    input_type = 'text'

    def __init__(self, key=None, label=None, validators=None, filters=None,
                 default=None, required=False, required_error=None,
                 params=None):
        def coerce(x):
            if x:
                x = x.strip()
                if x:
                    return x

        super().__init__(
            key=key,
            label=label,
            validators=validators,
            filters=filters,
            default=default,
            required=required,
            required_error=required_error,
            params=params,
            coerce=coerce,
        )
