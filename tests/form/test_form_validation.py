from forms_api.fields import IntegerField, StringField
from forms_api.form import Form
from tests import TestCase
from forms_api.validators import LengthValidator, NumberRangeValidator


class _Form(Form):
    field_string = StringField(
        validators=(LengthValidator(min=3, max=10),),
    )
    field_string_required = StringField(
        validators=(LengthValidator(min=5, max=50),),
        required=True,
    )
    field_integer = IntegerField(
        validators=(NumberRangeValidator(min=-10, max=10),),
    )
    field_integer_required = IntegerField(
        validators=(NumberRangeValidator(min=-10, max=10),),
        required=True,
    )


class TestFormValidation(TestCase):
    def test_failed(self):
        form = _Form()
        self.assertFalse(form.validate())
        self.assertIn(form.field_string_required.key, form.errors)
        self.assertIn(form.field_integer_required.key, form.errors)

    def test_for_required(self):
        dummy = _Form()

        form = _Form({
            dummy.field_string_required.key: '1' * 10,
            dummy.field_integer_required.key: 3,
        })
        self.assertTrue(form.validate())

    def test_failed_with_wrong_values(self):
        dummy = _Form()

        form = _Form({
            dummy.field_string.key: '1' * 11,
            dummy.field_string_required.key: '1' * 51,
            dummy.field_integer.key: 11,
            dummy.field_integer_required.key: -11,
        })
        self.assertFalse(form.validate())
        self.assertIn(dummy.field_string.key, form.errors)
        self.assertIn(dummy.field_string_required.key, form.errors)
        self.assertIn(dummy.field_integer.key, form.errors)
        self.assertIn(dummy.field_integer_required.key, form.errors)
