from forms_api.fields.base_field import Field
from forms_api.html import generate_checkbox


class BooleanField(Field):
    type = 'boolean'
    input_type = 'checkbox'

    def __init__(self, key=None, label=None, validators=None, default=None,
                 required=False, required_error=None, params=None):
        super().__init__(
            key=key,
            label=label,
            validators=validators,
            default=default,
            coerce=bool,
            required=required,
            required_error=required_error,
            params=params,
        )

    @property
    def value(self):
        return bool(super().value)

    def validate_required(self):
        if self.required is False and self.value is False:
            return True

        if self.required is True and self.value is False:
            self.error = self.get_required_error()
            return False

    def html(self, **attributes):
        return generate_checkbox(key=self.key, value=self.value, **attributes)
