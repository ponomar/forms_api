from copy import copy

from forms_api.fields.base_field import Field, check_params
from forms_api.fields.password_field import PasswordField


def _get_fields(form):
    fields, fields_keys = [], []
    for key in dir(form):
        value = getattr(form, key)
        if isinstance(value, Field):
            # We need to copy fields in form not to share their states between
            # different requests.
            value = copy(value)
            setattr(form, key, value)  # replace with copied one

            if not value.fld_key:
                value._set_key(key)

            fields.append(value)

            if value.key in fields_keys:
                raise ValueError(
                    'field with key `%s` already defined in %s '
                    'or it\'s parents' % (value.key, form)
                )

            fields_keys.append(value.key)

    fields.sort(key=lambda x: x._creation_counter)

    return tuple(fields)


class Form(object):
    fields = ()
    errors = None

    def __init__(self, formdata=None, object=None, params=None):
        check_params(params)

        self.object = object
        self.params = params
        self.fields = _get_fields(self)

        if formdata is not None:  # must be after fields assigning
            self.set_formdata(formdata)
        elif self.object:
            self.set_object_data()

    def set_formdata(self, formdata):
        for field in self.fields:
            if isinstance(field.value_empty, list):
                field.set_value(formdata.getlist(field.key))
            else:
                field.set_value(formdata.get(field.key))

    def set_object_data(self):
        for field in self.fields:
            if (
                hasattr(self.object, field.key)
                and not isinstance(field, PasswordField)
            ):
                field.set_value_from_object(getattr(self.object, field.key))

    def validate(self):
        errors = {}
        for field in self.fields:
            valid = field.validate(self)
            if not valid:
                errors[field.key] = field.error

        if not errors:
            errors = None

        self.errors = errors

        return not bool(self.errors)

    def schema(self):
        fields = [fld.schema() for fld in self.fields]

        result = dict(
            fields={f_['key']: f_ for f_ in fields},
            fields_keys=[f_['key'] for f_ in fields],
        )

        if self.params:
            params = dict()
            for k_, v_ in self.params.items():
                if callable(v_):
                    v_ = v_()

                params[k_] = v_

            result['params'] = params

        if self.errors:
            result['errors'] = self.errors

        return result
