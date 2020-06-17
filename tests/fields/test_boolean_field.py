from forms_api.fields.boolean_field import BooleanField
from tests.fields.utils import FieldTestCase


class TestBooleanField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=BooleanField,
            default=True,
            default_new=False,
            has_required=True,
        )

    def test_default_true(self):
        field = BooleanField(key=self.FIELD_KEY, default=True)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='boolean',
            input_type='checkbox',
            value=True,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="checkbox" name="{key}" id="{key}" '
                'checked="checked" class="cls">'
                ''.format(key=self.FIELD_KEY)
            ),
        )

    def test_default_false(self):
        field = BooleanField(key=self.FIELD_KEY, default=False)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='boolean',
            input_type='checkbox',
            value=False,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="checkbox" name="{key}" id="{key}" '
                'class="cls">'
                ''.format(key=self.FIELD_KEY)
            ),
        )
