from tests import TestCase
from tests.validators import DummyField
from forms_api.validators import NumberRangeValidator


class TestNumberRangeValidator(TestCase):
    def test(self):
        min, max, error = -100, 100.5, 'From -100 to 100.5.'

        validator = NumberRangeValidator(
            min=min,
            max=max,
            error=error,
        )
        self.assertEqual(validator.get_error(), error)
        self.assertJsonTypes(validator.schema())
        self.assertDictEqual(validator.schema(), dict(
            type='number',
            rule='range',
            min=min,
            max=max,
            error=error,
        ))
        self.assertEqual(validator(None, DummyField(min - 1)), error)
        self.assertIsNone(validator(None, DummyField(min)))
        self.assertIsNone(validator(None, DummyField(max - 1)))
        self.assertIsNone(validator(None, DummyField(max)))
        self.assertEqual(validator(None, DummyField(max + 1)), error)

    def test_failed_arguments(self):
        self.assertRaises(ValueError, NumberRangeValidator)
        self.assertRaises(ValueError, NumberRangeValidator, min=1, max=1)
        self.assertRaises(ValueError, NumberRangeValidator, min=2, max=1)

    def test_minimal(self):
        min, max = 1, 2
        error_1 = 'Must be not less than %d.' % min
        error_2 = 'Must be not greater than %d.' % max

        validator_1 = NumberRangeValidator(min=min)
        self.assertEqual(validator_1.get_error(), error_1)
        self.assertDictEqual(validator_1.schema(), dict(
            type='number',
            rule='range',
            min=min,
            error=error_1,
        ))
        self.assertEqual(validator_1(None, DummyField(min - 1)), error_1)
        self.assertIsNone(validator_1(None, DummyField(min)))

        validator_2 = NumberRangeValidator(max=max)
        self.assertEqual(validator_2.get_error(), error_2)
        self.assertDictEqual(validator_2.schema(), dict(
            type='number',
            rule='range',
            max=max,
            error=error_2,
        ))
