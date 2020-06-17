from forms_api.fields.string_field import StringField


class FileField(StringField):
    type = input_type = 'file'
