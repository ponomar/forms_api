from forms_api.fields.file_field import FileField
from tests.fields.utils import FieldTestCase


class TestFileField(FieldTestCase):
    def test_common(self):
        self.do_common(
            field_cls=FileField,
            default='   Test default    ',
            default_new='   Test default new   ',
        )

    def test(self):
        field = FileField(key=self.FIELD_KEY)
        self.assertTrue(field.validate(None))
        self.assertDictEqual(field.schema(), dict(
            key=self.FIELD_KEY,
            type='file',
            input_type='file',
            value=None,
            label=None,
        ))
        self.assertEqual(
            field.html(class_='cls'),
            (
                '<input type="file" name="{key}" id="{key}" '
                'value="" class="cls">'
                ''.format(key=self.FIELD_KEY)
            ),
        )
