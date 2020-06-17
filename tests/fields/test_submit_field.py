from forms_api.fields.submit_field import SubmitField
from tests.fields.utils import FieldTestCase


class TestSubmitField(FieldTestCase):
    def test_common(self):
        self.do_common(SubmitField)

    def test(self):
        field = SubmitField(key=self.FIELD_KEY)
        self.assertIsNone(field.value)
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='submit',
            input_type='submit',
            value=None,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="submit" name="{key}" id="{key}" class="cls">'
                ''.format(key=self.FIELD_KEY)
            ),
        )
