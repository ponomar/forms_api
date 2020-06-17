from forms_api.fields import StringField
from forms_api.form import Form
from tests import TestCase


class TestFieldsUniqueness(TestCase):
    def test_main(self):
        class _Form(Form):
            field_1 = StringField()
            field_2 = StringField()
            field_3 = StringField(key='field_1')

        self.assertRaises(ValueError, _Form)

    def test_fields_keys(self):
        class _Form(Form):
            field_1 = StringField()
            field_2 = StringField(key='field_3')

        form = _Form()
        self.assertEqual(form.field_1.key, 'field_1')
        self.assertEqual(form.field_2.key, 'field_3')
