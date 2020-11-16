from typing import Generator, Union

from forms_api.fields.base_field import null
from forms_api.fields.select_field import SelectField
from forms_api.html import generate_select


class SelectMultipleField(SelectField):
    type = 'select_multiple'
    value_empty = []

    def __init__(self, key=None, label=None, validators=None,
                 default: Union[list, tuple, None] = None, coerce=lambda x: x,
                 required=False, required_error=None, params=None, options=null,
                 error_not_in_options=null):
        super().__init__(
            key=key,
            label=label,
            validators=validators,
            options=options,
            default=default,
            required=required,
            required_error=required_error,
            error_not_in_options=error_not_in_options,
            params=params,
            coerce=coerce,
        )

    @property
    def value(self) -> list:
        if self.fld_value is not null:
            result = self.fld_value
        elif self.default is not None:
            result = self.default
        else:
            return self.value_empty

        result = [self.fld_coerce(i) for i in result]
        return [self.apply_filters(i) for i in result]

    @property
    def options(self) -> Generator:
        for key, label in self.get_options_iterator():
            selected = self.fld_coerce(key) in self.value
            yield [self.fld_coerce(key), label, selected]

    def _value_is_valid(self):
        keys = {k_ for k_, v_, s_ in self.options}
        return not keys or set(self.value).issubset(keys)

    def html(self, **attributes) -> str:
        return generate_select(
            key=self.key,
            options=self.options,
            multiple=True,
            **attributes,
        )
