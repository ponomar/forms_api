from forms_api.fields.base_field import Field
from forms_api.html import generate_submit


class SubmitField(Field):
    type = input_type = 'submit'

    def __init__(self, key=None, label=None, params=None):
        super().__init__(key=key, label=label, params=params)

    def html(self, **attributes):
        return generate_submit(key=self.key, **attributes)
