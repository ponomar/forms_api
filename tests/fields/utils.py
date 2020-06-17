from forms_api.fields.base_field import ERROR_REQUIRED
from tests import TestCase


class FieldTestCase(TestCase):
    FIELD_KEY = 'test-key'

    def _do_label(self, field):
        self.assertIsNone(field.label)

        label = 'Test label'
        field.set_label(lambda: label)
        self.assertEqual(field.label, label)

        label_new = '%s new' % label
        field.set_label(label_new)
        self.assertEqual(field.label, label_new)

    def _do_default(self, field, default, default_new):
        self.assertIsNone(field.default)

        field.set_default(lambda: default)
        self.assertEqual(field.default, default)

        field.set_default(default_new)
        self.assertEqual(field.value, field.fld_coerce(default_new))
        field.set_default(None)  # cleanup

    def _do_coerce(self, field, coerce):
        field.set_coerce(coerce)
        self.assertIs(field.fld_coerce, coerce)

        coerce_new = lambda x: coerce(x)
        field.set_coerce(coerce_new)
        self.assertIs(field.fld_coerce, coerce_new)

    def _do_validators(self, field):
        self.assertIsNone(field.fld_validators)

        validators = (1, 2, 3)
        field.set_validators(validators)
        self.assertEqual(field.fld_validators, validators)

        validators_new = (4, 5, 6)
        field.set_validators(validators_new)
        self.assertEqual(field.fld_validators, validators_new)
        field.set_validators(None)  # cleanup

    def _do_filters(self, field):
        self.assertIsNone(field.fld_filters)

        filters = (1, 2, 3)
        field.set_filters(filters)
        self.assertEqual(field.fld_filters, filters)

        filters_new = (4, 5, 6)
        field.set_filters(filters_new)
        self.assertEqual(field.fld_filters, filters_new)
        field.set_filters(None)  # cleanup

    def _do_required(self, field):
        self.assertIs(field.required, False)
        self.assertIs(field.validate(None), True)
        schema = field.schema()
        self.assertNotIn('required', schema)
        self.assertNotIn('required_error', schema)

        field.set_required(True)
        self.assertIs(field.required, True)
        self.assertIs(field.schema()['required'], True)
        self.assertIs(field.validate(None), False)
        schema = field.schema()
        self.assertIs(schema['required'], True)
        self.assertEqual(schema['required_error'], ERROR_REQUIRED)

        required_error = 'Required Error'
        field.set_required_error(required_error)
        self.assertEqual(field.get_required_error(), required_error)

        required_error_new = '%s new' % required_error
        field.set_required_error(lambda: required_error_new)
        self.assertEqual(field.get_required_error(), required_error_new)

    def _do_key_absent(self, field_cls):
        field = field_cls()
        self.assertRaises(ValueError, field.schema)

    def _do_minimal(self, field_cls):
        field_minimal = field_cls(key=self.FIELD_KEY)
        self.assertTrue(field_minimal.validate(None))
        self.assertJsonTypes(field_minimal.schema())

    def _do_params(self, field):
        self.assertEqual(field.params, {})

        params = dict(help='Test help', description='Test Description')
        field.set_params(params)
        self.assertEqual(field.params, params)

        params_new = dict(help='Test help new')
        field.set_params(params_new)
        self.assertEqual(field.params, params_new)

        params_not_valid_keys = {12: 'test'}
        self.assertRaises(TypeError, field.set_params, params_not_valid_keys)
        params_not_valid_type = []
        self.assertRaises(TypeError, field.set_params, params_not_valid_type)

    def do_common(self, field_cls, default=None, default_new=None,
                  has_validators=False, has_filters=False, has_required=False,
                  coerce=None):
        field = field_cls(key=self.FIELD_KEY)
        self.assertEqual(field.key, self.FIELD_KEY)
        self.assertJsonTypes(field.schema())
        self.assertIsInstance(field.html(), str)
        self.assertRaises(ValueError, field.html, id='id')
        self.assertRaises(ValueError, field.html, name='id')
        self.assertRaises(ValueError, field.html, type='id')

        self._do_label(field)
        self._do_params(field)
        self._do_key_absent(field_cls)
        self._do_minimal(field_cls)

        if coerce is not None:
            self._do_coerce(field, coerce)
        if default_new is not None:
            self._do_default(field, default, default_new)
        if has_validators:
            self._do_validators(field)
        if has_filters:
            self._do_filters(field)
        if has_required:
            self._do_required(field)
