from forms_api.fields.hidden_field import HiddenField
from tests.fields.utils import FieldTestCase


class TestHiddenField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=HiddenField,
            default='   Test default    ',
            default_new='   Test default new   ',
            has_required=True,
            has_filters=True,
            has_validators=True,
        )

    def test(self):
        default = '   Test default    '

        field = HiddenField(key=self.FIELD_KEY, default=default)
        self.assertEqual(field.value, default.strip())
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='hidden',
            input_type='hidden',
            value=default.strip(),
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="hidden" name="{key}" id="{key}" '
                'value="{value}" class="cls">'
                ''.format(key=self.FIELD_KEY, value=default.strip())
            ),
        )
