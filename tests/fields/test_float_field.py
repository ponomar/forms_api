from forms_api.fields.base_field import ERROR_REQUIRED
from forms_api.fields.float_field import (
    ERROR_NOT_VALID_FLOAT,
    FloatField,
    coerce_float
)
from tests.fields.utils import FieldTestCase
from forms_api.validators import NumberRangeValidator


class TestFloatField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=FloatField,
            default=1.2,
            default_new=2,
            coerce=coerce_float,
        )

    def test(self):
        default = 0.0

        field = FloatField(key=self.FIELD_KEY, default=default)
        self.assertEqual(field.value, default)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='float',
            input_type='number',
            value=default,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="number" name="{key}" id="{key}" value="{value}" class="cls">'
                ''.format(key=self.FIELD_KEY, value=default)
            ),
        )

    def test_bad_input(self):
        field = FloatField(key=self.FIELD_KEY)
        field.set_value('1a')
        field.schema()

    def test_required(self):
        field = FloatField(key=self.FIELD_KEY, required=True)
        self.assertIsNone(field.error)
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_REQUIRED)
        field.set_value('1.2')
        self.assertTrue(field.validate(None))
        self.assertIsNone(field.error)
        field.set_value(1.2)
        self.assertEqual(field.value, 1.2)
        self.assertTrue(field.validate(None))
        self.assertIsNone(field.error)
        field.set_value(1)
        self.assertTrue(field.validate(None))
        self.assertIsNone(field.error)
        field.set_value('1.0a')
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_NOT_VALID_FLOAT)

    def test_ndigits(self):
        field = FloatField(key=self.FIELD_KEY, ndigits=2)
        self.assertIsNone(field.error)
        field.set_value('1.2')
        self.assertEqual(field.value, 1.2)
        field.set_value('1.223')
        self.assertEqual(field.value, 1.22)
        field.set_value(1)
        self.assertEqual(field.value, 1.0)
        field.set_value(1.235)
        self.assertEqual(field.value, 1.24)

    def test_number_range_validator(self):
        field = FloatField(
            key=self.FIELD_KEY,
            validators=(NumberRangeValidator(min=-100, max=100),),
            required=True,
        )
        field.set_value('-101')  # error, too small
        self.assertFalse(field.validate(None))
        field.set_value('-100')  # ok, bottom boundary
        field.validate(None)
        self.assertTrue(field.validate(None))
        field.set_value('10')  # ok
        self.assertTrue(field.validate(None))
        field.set_value('100')  # ok, top boundary
        self.assertTrue(field.validate(None))
        field.set_value('101')  # error, too big
        self.assertFalse(field.validate(None))
