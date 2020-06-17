from forms_api.fields import StringField
from forms_api.form import Form
from tests import TestCase
from forms_api.validators import EqualToValidator


_ERROR_NOT_EQUAL = 'Error not equal.'
_ERROR_FIELD_NOT_EXISTS = 'Error field does not exist.'


class TestEqualToValidator(TestCase):
    def test_schema(self):
        validator = EqualToValidator(
            fieldname='password',
            error=_ERROR_NOT_EQUAL,
            error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
        )
        self.assertDictEqual(validator.schema(), dict(
            type='equal_to',
            fieldname='password',
            error=_ERROR_NOT_EQUAL,
        ))

    def test(self):
        validator = EqualToValidator(
            fieldname='password',
            error=_ERROR_NOT_EQUAL,
            error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
        )

        class _Form(Form):
            password = StringField()
            password2 = StringField(validators=(validator,))

        form = _Form(dict(password='xxxxx', password2='xxxxx'))
        self.assertTrue(form.validate())

    def test_error_not_equal(self):
        validator = EqualToValidator(
            fieldname='password',
            error=lambda: _ERROR_NOT_EQUAL,
            error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
        )

        class _Form(Form):
            password = StringField()
            password2 = StringField(validators=(validator,))

        form = _Form(dict(password='xxxxx', password2='yyyyy'))
        self.assertFalse(form.validate())
        self.assertEqual(form.errors[form.password2.key], _ERROR_NOT_EQUAL)

    def test_error_field_not_exists(self):
        validator = EqualToValidator(
            fieldname='password3',
            error=_ERROR_NOT_EQUAL,
            error_field_not_exists=_ERROR_FIELD_NOT_EXISTS,
        )

        class _Form(Form):
            password = StringField()
            password2 = StringField(validators=(validator,))

        form = _Form(dict(password='xxxxx', password2='xxxxx'))
        self.assertFalse(form.validate())
        self.assertEqual(
            form.errors[form.password2.key],
            _ERROR_FIELD_NOT_EXISTS,
        )

    def test_error_field_not_exists_lazy_error(self):
        validator = EqualToValidator(
            fieldname='password3',
            error=_ERROR_NOT_EQUAL,
            error_field_not_exists=lambda: _ERROR_FIELD_NOT_EXISTS,
        )

        class _Form(Form):
            password = StringField()
            password2 = StringField(validators=(validator,))

        form = _Form(dict(password='xxxxx', password2='xxxxx'))
        self.assertFalse(form.validate())
        self.assertEqual(
            form.errors[form.password2.key],
            _ERROR_FIELD_NOT_EXISTS,
        )
