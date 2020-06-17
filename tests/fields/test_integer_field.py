from forms_api.fields.base_field import ERROR_REQUIRED
from forms_api.fields.integer_field import (
    ERROR_NOT_VALID_INTEGER,
    IntegerField,
    coerce_int
)
from tests.fields.utils import FieldTestCase
from forms_api.validators import NumberRangeValidator


class TestIntegerField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=IntegerField,
            default=1,
            default_new=2,
            coerce=coerce_int,
        )

    def test(self):
        default = 0

        field = IntegerField(key=self.FIELD_KEY, default=default)
        self.assertEqual(field.value, default)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='integer',
            input_type='number',
            value=default,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="number" name="{key}" id="{key}" value="{value}" '
                'class="cls">'
                ''.format(key=self.FIELD_KEY, value=default)
            ),
        )

    def test_bad_input(self):
        field = IntegerField(key=self.FIELD_KEY)
        field.set_value('1a')
        field.schema()

    def test_required(self):
        field = IntegerField(key=self.FIELD_KEY, required=True)
        self.assertIsNone(field.error)
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_REQUIRED)
        field.set_value('1.2')
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_NOT_VALID_INTEGER)
        field.set_value(1.2)
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_NOT_VALID_INTEGER)

    def test_number_range_validator(self):
        field = IntegerField(
            key=self.FIELD_KEY,
            validators=(NumberRangeValidator(min=-100, max=100),),
            required=True,
        )
        field.set_value('-101')  # error, too small
        self.assertFalse(field.validate(None))
        field.set_value('-100')  # ok, bottom boundary
        self.assertTrue(field.validate(None))
        field.set_value('10')  # ok
        self.assertTrue(field.validate(None))
        field.set_value('100')  # ok, top boundary
        self.assertTrue(field.validate(None))
        field.set_value('101')  # error, too big
        self.assertFalse(field.validate(None))
