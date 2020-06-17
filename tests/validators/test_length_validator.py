from tests import TestCase
from tests.validators import DummyField
from forms_api.validators import LengthValidator


class TestLengthValidator(TestCase):
    def test(self):
        min, max = 1, 100
        error, error_count = 'From 1 to 100.', 'typed %d'

        validator = LengthValidator(
            min=min,
            max=max,
            error=error,
            error_count=error_count,
        )
        self.assertEqual(validator.get_error(), error)
        self.assertEqual(
            validator.get_error(12),
            '%s %s' % (error, error_count % 12),
        )
        self.assertJsonTypes(validator.schema())
        self.assertDictEqual(validator.schema(), dict(
            type='string',
            rule='length',
            min=min,
            max=max,
            error=error,
        ))
        self.assertEqual(
            validator(None, DummyField('', required=True)),
            '%s %s' % (error, error_count % 0),
        )
        self.assertIsNone(validator(None, DummyField('1' * min)))
        self.assertIsNone(validator(None, DummyField('1' * (max - 1))))
        self.assertIsNone(validator(None, DummyField('1' * max)))
        self.assertEqual(
            validator(None, DummyField('1' * (max + 1))),
            '%s %s' % (error, error_count % (max + 1)),
        )

    def test_failed_arguments(self):
        self.assertRaises(ValueError, LengthValidator)
        self.assertRaises(ValueError, LengthValidator, min=-1)
        self.assertRaises(ValueError, LengthValidator, min=1, max=1)
        self.assertRaises(ValueError, LengthValidator, min=2, max=1)
        self.assertRaises(ValueError, LengthValidator, max=0)

    def test_minimal(self):
        min, max = 1, 2

        validator_1 = LengthValidator(min=min)
        self.assertEqual(
            validator_1.get_error(),
            'Must be from %d symbols.' % min,
        )
        self.assertDictEqual(validator_1.schema(), dict(
            type='string',
            rule='length',
            min=min,
            error='Must be from %d symbols.' % min,
        ))

        validator_2 = LengthValidator(max=max)
        self.assertEqual(
            validator_2.get_error(),
            'Must be up to %d symbols.' % max,
        )
        self.assertDictEqual(validator_2.schema(), dict(
            type='string',
            rule='length',
            max=max,
            error='Must be up to %d symbols.' % max,
        ))
