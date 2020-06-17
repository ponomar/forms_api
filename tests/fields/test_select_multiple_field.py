from forms_api.fields.select_multiple_field import SelectMultipleField
from tests.fields.utils import FieldTestCase


class TestSelectMultipleField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=SelectMultipleField,
            default=['1'],
            default_new=['2'],
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
        default = ['2', '3']

        field = SelectMultipleField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
        )
        schema = field.schema()
        self.assertListEqual(schema['value'], default)
        self.assertListEqual(
            schema['options'],
            [[k_, v_, k_ in default] for k_, v_ in options],
        )
        self.assertEqual(
            field.html(class_='cls'),
            (
                f'<select name="{self.FIELD_KEY}" id="{self.FIELD_KEY}" '
                f'class="cls" multiple>'
                f'<option value="">Title</option>'
                f'<option value="1">First option</option>'
                f'<option value="2" selected="selected">Second option</option>'
                f'<option value="3" selected="selected">Third option</option>'
                f'</select>'
            ),
        )

    def test_without_default(self):
        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]

        field = SelectMultipleField(key=self.FIELD_KEY, options=lambda: options)
        schema = field.schema()
        self.assertListEqual(schema['value'], [])
        self.assertListEqual(
            schema['options'],
            [[k_, v_, False] for k_, v_ in options],
        )

    def test_without_default_with_updated_value(self):
        options = [
            [None, 'Title'],
            ['1', 'First option'],
            ['2', 'Second option'],
            ['3', 'Third option'],
        ]

        field = SelectMultipleField(key=self.FIELD_KEY, options=lambda: options)
        schema = field.schema()
        self.assertListEqual(schema['value'], [])
        self.assertListEqual(
            schema['options'],
            [[k_, v_, False] for k_, v_ in options],
        )

        value = ['2']
        field.set_value(value)
        schema = field.schema()
        self.assertListEqual(schema['value'], value)
        self.assertListEqual(
            schema['options'],
            [[k_, v_, k_ == value[0]] for k_, v_ in options],
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
        default = ['2']

        field = SelectMultipleField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
            coerce=coerce,
        )
        schema = field.schema()
        self.assertListEqual(schema['value'], [int(default[0])])
        self.assertListEqual(
            schema['options'],
            [
                [
                    field.fld_coerce(k_),
                    v_,
                    field.fld_coerce(k_) == int(default[0])
                ]
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
        default = [2]

        field = SelectMultipleField(
            key=self.FIELD_KEY,
            options=lambda: options,
            default=default,
            coerce=coerce,
        )
        schema = field.schema()
        self.assertListEqual(schema['value'], default)
        self.assertListEqual(
            schema['options'],
            [[k_, v_, k_ in default] for k_, v_ in options],
        )
