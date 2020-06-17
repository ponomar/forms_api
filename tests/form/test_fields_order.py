from forms_api.fields import StringField
from forms_api.form import Form
from tests import TestCase


class TestFieldsOrder(TestCase):
    @staticmethod
    def get_form_main_cls():
        class FormMain(Form):
            field_s1f = StringField()
            field_d2g = StringField()
            field_a3q = StringField()
            field_v4e = StringField()
            field_k5a = StringField()
            field_j6h = StringField()
            field_r7u = StringField()
            field_e8y = StringField()
            field_l9n = StringField()
            field_t10b = StringField()

        return FormMain

    def test_form_main(self):
        FormMain = self.get_form_main_cls()
        form = FormMain()

        self.assertEqual(len(form.fields), 10)

        for field in form.fields:
            self.assertIsNotNone(field.key)

        self.assertEqual(form.fields[0].key, form.field_s1f.key)
        self.assertEqual(form.fields[1].key, form.field_d2g.key)
        self.assertEqual(form.fields[2].key, form.field_a3q.key)
        self.assertEqual(form.fields[3].key, form.field_v4e.key)
        self.assertEqual(form.fields[4].key, form.field_k5a.key)
        self.assertEqual(form.fields[5].key, form.field_j6h.key)
        self.assertEqual(form.fields[6].key, form.field_r7u.key)
        self.assertEqual(form.fields[7].key, form.field_e8y.key)
        self.assertEqual(form.fields[8].key, form.field_l9n.key)
        self.assertEqual(form.fields[9].key, form.field_t10b.key)

    def test_form_inherited(self):
        class FormInherited(self.get_form_main_cls()):
            field_x11p = StringField()
            field_o12s = StringField()
            field_y13z = StringField()

        form = FormInherited()

        self.assertEqual(len(form.fields), 13)

        for field in form.fields:
            self.assertIsNotNone(field.key)

        self.assertEqual(form.fields[0].key, form.field_s1f.key)
        self.assertEqual(form.fields[1].key, form.field_d2g.key)
        self.assertEqual(form.fields[2].key, form.field_a3q.key)
        self.assertEqual(form.fields[3].key, form.field_v4e.key)
        self.assertEqual(form.fields[4].key, form.field_k5a.key)
        self.assertEqual(form.fields[5].key, form.field_j6h.key)
        self.assertEqual(form.fields[6].key, form.field_r7u.key)
        self.assertEqual(form.fields[7].key, form.field_e8y.key)
        self.assertEqual(form.fields[8].key, form.field_l9n.key)
        self.assertEqual(form.fields[9].key, form.field_t10b.key)
        self.assertEqual(form.fields[10].key, form.field_x11p.key)
        self.assertEqual(form.fields[11].key, form.field_o12s.key)
        self.assertEqual(form.fields[12].key, form.field_y13z.key)
