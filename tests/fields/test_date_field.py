from datetime import date, datetime

from forms_api.fields.base_field import ERROR_REQUIRED
from forms_api.fields.date_field import (
    ERROR_NOT_VALID_DATE,
    DateField,
    coerce_date
)
from tests.fields.utils import FieldTestCase


class TestDateField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=DateField,
            default=date(2018, 1, 2),
            default_new=date(2018, 1, 3),
            coerce=coerce_date,
        )

    def test(self):
        default = date(2018, 1, 1)

        field = DateField(key=self.FIELD_KEY, default=default)
        self.assertEqual(field.value, default)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='date',
            input_type='date',
            value='2018-01-01',
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="date" name="{key}" id="{key}" value="{value}" class="cls">'
                ''.format(key=self.FIELD_KEY, value=default)
            ),
        )

    def test_bad_input(self):
        field = DateField(key=self.FIELD_KEY)
        field.set_value('1a')
        field.schema()

    def test_required(self):
        field = DateField(key=self.FIELD_KEY, required=True)
        self.assertIsNone(field.error)
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_REQUIRED)
        field.set_value('2018-01-05')
        self.assertTrue(field.validate(None))
        self.assertIsNone(field.error)
        field.set_value(date(2018, 4, 1))
        self.assertTrue(field.validate(None))
        self.assertIsNone(field.error)
        field.set_value('1.0a')
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_NOT_VALID_DATE)
        field.set_value(datetime(2018, 1, 1))
        self.assertFalse(field.validate(None))
        self.assertEqual(field.error, ERROR_NOT_VALID_DATE)

    def test_value_schema(self):
        field = DateField(key=self.FIELD_KEY, required=True)
        field.set_value(date(2018, 1, 10))
        self.assertEqual(field.schema()['value'], '2018-01-10')
