from forms_api.fields.string_field import StringField


class HiddenField(StringField):
    type = input_type = 'hidden'
