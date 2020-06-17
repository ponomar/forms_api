from forms_api.fields.select_field import SelectField
from tests.fields.utils import FieldTestCase


class TestSelectField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=SelectField,
            default='1',
            default_new='2',
            coerce=lambda x: x,
            has_validators=True,
            has_required=True,
        )

    def test_with_default(self):
        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]
        default = '2'

        field = SelectField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
        )
        schema = field.schema()
        self.assertEqual(schema['value'], default)
        self.assertEqual(
            schema['options'],
            [[k_, v_, k_ == default] for k_, v_ in options],
        )
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<select name="{key}" id="{key}" class="cls">'
                '<option value="">Title</option>'
                '<option value="1">First option</option>'
                '<option value="2" selected="selected">Second option</option>'
                '<option value="3">Third option</option>'
                '</select>'.format(key=self.FIELD_KEY)
            ),
        )

    def test_without_default(self):
        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]

        field = SelectField(key=self.FIELD_KEY, options=lambda: options)
        schema = field.schema()
        self.assertIsNone(schema['value'])
        self.assertEqual(
            schema['options'],
            [[k_, v_, k_ is None] for k_, v_ in options],
        )

    def test_without_default_with_updated_value(self):
        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]

        field = SelectField(key=self.FIELD_KEY, options=lambda: options)
        schema = field.schema()
        self.assertIsNone(schema['value'])
        self.assertEqual(
            schema['options'],
            [[k_, v_, k_ is None] for k_, v_ in options],
        )

        value = '2'
        field.set_value(value)
        schema = field.schema()
        self.assertEqual(schema['value'], value)
        self.assertEqual(
            schema['options'],
            [[k_, v_, k_ == value] for k_, v_ in options],
        )

    def test_with_coerce_int(self):
        def coerce(x):
            if x in ('', None):
                return x

            return int(x)

        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]
        default = '2'

        field = SelectField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
            coerce=coerce,
        )
        schema = field.schema()
        self.assertEqual(schema['value'], int(default))
        self.assertEqual(
            schema['options'],
            [
                [field.fld_coerce(k_), v_, field.fld_coerce(k_) == int(default)]
                for k_, v_ in options
            ],
        )

    def test_with_coerce_int_as_integers(self):
        def coerce(x):
            if x in ('', None):
                return x

            return int(x)

        options = [
            [None, 'Title'],
            [1, 'First option'],
            [2, 'Second option'],
            [3, 'Third option'],
        ]
        default = 2

        field = SelectField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
            coerce=coerce,
        )
        schema = field.schema()
        self.assertEqual(schema['value'], default)
        self.assertEqual(
            schema['options'],
            [[k_, v_, k_ == default] for k_, v_ in options],
        )
