from forms_api.fields.textarea_field import TextAreaField
from tests.fields.utils import FieldTestCase


class TestTextAreaField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=TextAreaField,
            default='   Test default    ',
            default_new='   Test default new   ',
            has_validators=True,
            has_filters=True,
            has_required=True,
        )

    def test(self):
        default = '   Test default    '

        field = TextAreaField(key=self.FIELD_KEY, default=default)
        self.assertEqual(field.value, default.strip())
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='text',
            input_type='textarea',
            value=default.strip(),
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<textarea name="{key}" id="{key}" class="cls">'
                '{value}</textarea>'
                ''.format(key=self.FIELD_KEY, value=default.strip())
            ),
        )
        self.assertEqual(
            field.html(rows=5),
            (
                '<textarea name="{key}" id="{key}" rows="5">{value}</textarea>'
                ''.format(key=self.FIELD_KEY, value=default.strip())
            ),
        )

    def test_minimal(self):
        field = TextAreaField(key=self.FIELD_KEY)
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='text',
            input_type='textarea',
            value=None,
            label=None,
        ))
        self.assertEqual(
            field.html(),
            (
                '<textarea name="{key}" id="{key}"></textarea>'
                ''.format(key=self.FIELD_KEY)
            ),
        )
