from forms_api.fields.base_field import ERROR_REQUIRED
from forms_api.fields.string_field import StringField
from tests.fields.utils import FieldTestCase
from forms_api.validators import LengthValidator


class TestStringField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=StringField,
            default='   Test default    ',
            default_new='   Test default new   ',
            has_validators=True,
            has_filters=True,
            has_required=True,
        )

    def test(self):
        label = 'Test Label'

        field = StringField(key=self.FIELD_KEY, label=lambda: label)
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='string',
            input_type='text',
            value=None,
            label=label,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="text" name="{key}" id="{key}" value="" '
                'class="cls">'
                ''.format(key=self.FIELD_KEY)
            ),
        )

    def test_length_validator(self):
        field_1 = StringField(key=self.FIELD_KEY, required=True)
        self.assertIsNone(field_1.error)
        self.assertFalse(field_1.validate(None))
        self.assertEqual(field_1.error, ERROR_REQUIRED)

        field_2 = StringField(key=self.FIELD_KEY, required=False)
        self.assertIsNone(field_2.error)
        self.assertTrue(field_2.validate(None))
        self.assertIsNone(field_2.error)

        field_3 = StringField(
            key=self.FIELD_KEY,
            validators=(LengthValidator(min=5, max=10),),
        )
        self.assertTrue(field_3.validate(None))  # ok, because not required

        field_4 = StringField(
            key=self.FIELD_KEY,
            validators=(LengthValidator(min=5, max=10),),
            required=True,
        )
        self.assertFalse(field_4.validate(None))  # required, but empty
        field_4.set_value('1' * 5)
        self.assertTrue(field_4.validate(None))  # ok, 5-symbols text
        field_4.set_value('1' * 15)
        self.assertFalse(field_4.validate(None))  # error, too big
        field_4.set_value('1' * 7)
        self.assertTrue(field_4.validate(None))  # ok, 7-symbols text

    def test_filters(self):
        default = 'Some text. Another text.   '

        field = StringField(
            key=self.FIELD_KEY,
            default=default,
            filters=(
                lambda x: x.lower(),
                lambda x: x.replace('a', 'b'),
            ),
        )
        self.assertEqual(field.value, default.strip().lower().replace('a', 'b'))
