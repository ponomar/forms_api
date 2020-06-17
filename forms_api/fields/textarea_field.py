from forms_api.fields.string_field import StringField
from forms_api.html import generate_textarea


class TextAreaField(StringField):
    type = 'text'
    input_type = 'textarea'

    def html(self, **attributes):
        return generate_textarea(key=self.key, value=self.value, **attributes)
