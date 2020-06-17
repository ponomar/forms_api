from forms_api.fields import StringField
from forms_api.form import Form
from tests import TestCase


class TestFieldsStateNotShared(TestCase):
    def test(self):
        key1, key2 = 'key1', 'key2'

        class FormClass(Form):
            field1 = StringField(key=key1)
            field2 = StringField(key=key2)

        form1 = FormClass()
        self.assertEqual(form1.field1.key, key1)
        self.assertEqual(form1.field2.key, key2)
        form2 = FormClass()
        self.assertEqual(form2.field1.key, key1)
        self.assertEqual(form2.field2.key, key2)

        key1_new, key2_new = 'key1_new', 'key2_new'
        form1.field1._set_key(key1_new)
        form1.field2._set_key(key2_new)
        self.assertEqual(form1.field1.key, key1_new)  # new state
        self.assertEqual(form1.field2.key, key2_new)
        self.assertEqual(FormClass.field1.key, key1)  # old state
        self.assertEqual(FormClass.field2.key, key2)
        self.assertEqual(form2.field1.key, key1)      # old state
        self.assertEqual(form2.field2.key, key2)
