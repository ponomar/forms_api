from typing import Optional

from forms_api.html import generate_input


ERROR_REQUIRED = 'This field is required.'
ERROR_NOT_VALID = 'Format not valid.'


class _Null(object):
    def __repr__(self):
        return '<null>'

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False


null = _Null()


def check_params(params):
    if isinstance(params, dict):
        for k_, v_ in params.items():
            if not isinstance(k_, str):
                raise TypeError('`params` keys must be <string>')
            if not (
                isinstance(v_, (str, type(None), bool, int, float))
                or callable(v_)
            ):
                raise TypeError(
                    '`params` values must be <str>, <int>, <float>, <None>, <bool> or callable'
                )
    elif params is not None:
        raise TypeError('`params` must be None or <dict>')


class Field(object):
    type: str
    input_type: str

    _creation_counter: int = 0

    required: bool = False
    error: Optional[str] = None
    fld_key: str
    fld_value = null
    fld_label = null
    fld_validators = null
    fld_filters = null
    fld_default = null
    fld_params = null
    fld_coerce = null
    fld_required_error = null
    fld_not_valid_error = null
    value_empty = None

    def __init__(self, key=None, label=None, validators=None, filters=None,
                 default=None, coerce=lambda x: x, required=False,
                 required_error=None, not_valid_error=null, params=None):
        self.fld_key = key
        self.set_label(label)
        self.set_validators(validators)
        self.set_filters(filters)
        self.set_default(default)
        self.set_params(params)
        self.set_coerce(coerce)
        self.set_required(required)
        self.set_required_error(required_error)
        self.set_not_valid_error(not_valid_error)

        # Simple hack to save fields order
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

    def _set_key(self, value):
        """The form will set it on form initialization"""
        self.fld_key = value

    @property
    def key(self):
        if not self.fld_key:
            raise ValueError('can\'t get field key, it\'s not ready')

        return self.fld_key

    def set_value(self, value):
        """The form will set it on form initialization if formdata provided"""
        self.fld_value = value

    def set_value_from_object(self, value):
        """The form will set it on form initialization if formdata is None"""
        if value is not None and callable(self.fld_coerce):
            value = self.fld_coerce(value)

        self.fld_value = value

    @property
    def label(self):
        if callable(self.fld_label):
            value = self.fld_label()
        else:
            value = self.fld_label

        if not value:
            value = None

        return value

    @property
    def default(self):
        if callable(self.fld_default):
            return self.fld_default()

        return self.fld_default

    def apply_filters(self, value):
        for flt in self.fld_filters or ():
            if value is None:
                break

            value = flt(value)

        return value

    @property
    def value(self):
        if self.fld_value is not null:
            result = self.fld_value
        elif self.default is not None:
            result = self.default
        else:
            return

        try:
            result = self.fld_coerce(result)
        except Exception:
            self.error = self.get_not_valid_error()
            return

        result = self.apply_filters(result)
        if result == '':
            result = None

        return result

    @property
    def value_schema(self):
        return self.value

    def set_label(self, value):
        self.fld_label = value

    def set_default(self, value):
        self.fld_default = value

    def set_validators(self, value):
        """
        Validators must be of immutable ordered type (e.g. <tuple>) or None.
        <list> is error prone because of it's mutability while
        appending validators to existent ones, so they can silently growth
        to infinite size.
        """
        if not isinstance(value, (tuple, type(None))):
            raise TypeError

        self.fld_validators = value

    def set_filters(self, value):
        """See set_validators()"""
        if not isinstance(value, (tuple, type(None))):
            raise TypeError

        self.fld_filters = value

    def set_required(self, value):
        if not isinstance(value, bool):
            raise TypeError

        self.required = value

    def set_required_error(self, value):
        self.fld_required_error = value

    def set_not_valid_error(self, value):
        self.fld_not_valid_error = value

    def set_params(self, value):
        check_params(value)
        self.fld_params = value

    def set_coerce(self, value):
        self.fld_coerce = value

    @property
    def params(self):
        return self.fld_params or {}

    def get_required_error(self):
        if callable(self.fld_required_error):
            result = self.fld_required_error()
        else:
            result = self.fld_required_error

        return result or ERROR_REQUIRED

    def get_not_valid_error(self):
        if callable(self.fld_not_valid_error):
            result = self.fld_not_valid_error()
        else:
            result = self.fld_not_valid_error

        return result or ERROR_NOT_VALID

    def validate_required(self):
        if (
            self.required is False
            and self.value == self.value_empty
            and not self.fld_validators
        ):
            return True

        if self.required is True and self.value == self.value_empty:
            self.error = self.get_required_error()
            return False

    def validate(self, form) -> bool:
        self.error = None
        value = self.value  # Required line! To create coerce not_valid_error if needed
        if self.error:
            return False

        required_valid = self.validate_required()
        if required_valid is not None:
            return required_valid

        for validator in self.fld_validators or ():
            error = validator(form=form, field=self)
            if error:
                self.error = error
                return False

        return True

    def schema(self) -> dict:
        result = dict(
            key=self.key,
            type=self.type,
            input_type=self.input_type,
            value=self.value_schema,
            label=self.label,
        )

        if self.params:
            params = dict()
            for k_, v_ in self.params.items():
                if callable(v_):
                    v_ = v_()

                params[k_] = v_

            result['params'] = params

        if self.required:
            result['required'] = True
            result['required_error'] = self.get_required_error()

        if self.fld_validators:
            result['validators'] = [
                v_.schema() for v_ in self.fld_validators
                if hasattr(v_, 'schema')
            ]

        if self.error:
            result['error'] = self.error

        return result

    def html(self, **attributes) -> str:
        return generate_input(
            input_type=self.input_type,
            key=self.key,
            value=self.value,
            **attributes
        )
