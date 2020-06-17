from forms_api.fields.string_field import StringField


class PasswordField(StringField):
    type = input_type = 'password'
