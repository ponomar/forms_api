from tests import TestCase
from tests.validators import DummyField
from forms_api.validators import EmailValidator


class TestEmailValidator(TestCase):
    def test(self):
        error = 'Invalid Email.'

        validator = EmailValidator(error)
        self.assertEqual(validator.get_error(), error)
        schema = validator.schema()
        self.assertJsonTypes(schema)
        self.assertEqual(schema['type'], 'regex')
        self.assertEqual(schema['error'], error)
        self.assertEqual(validator(None, DummyField('')), error)
        self.assertEqual(validator(None, DummyField('example.com')), error)
        self.assertEqual(validator(None, DummyField('a@@example.com')), error)
        self.assertEqual(validator(None, DummyField('a@b@example.com')), error)
        self.assertEqual(validator(None, DummyField('a@example')), error)
        self.assertEqual(validator(None, DummyField('a@example.')), error)
        self.assertEqual(validator(None, DummyField('a@.com')), error)
        self.assertEqual(validator(None, DummyField('a+1@b.com')), error)
        self.assertEqual(validator(None, DummyField('ab c@b.com')), error)
        self.assertEqual(validator(None, DummyField('abc@b c.com')), error)
        self.assertEqual(validator(None, DummyField('abc@bc.c om')), error)
        self.assertEqual(validator(None, DummyField('abc@bc..com')), error)
        self.assertEqual(validator(None, DummyField('abcф@bc.com')), error)
        self.assertIsNone(validator(None, DummyField('abc@ex.am.p.l.e.com')))
        self.assertIsNone(validator(None, DummyField('abc@example.com')))
        self.assertIsNone(validator(None, DummyField('a@b.co')))
