from forms_api.validators.base_validator import Validator


class EqualToValidator(Validator):
    def __init__(self, fieldname, error=None, error_field_not_exists=None):
        assert isinstance(fieldname, str)
        self.fieldname = fieldname
        self.error = error or 'Must be equal to %s.' % fieldname
        self.error_field_not_exists = (
            error_field_not_exists
            or 'Invalid field name %s.' % fieldname
        )

    def schema(self):
        return dict(
            type='equal_to',
            fieldname=self.fieldname,
            error=self.get_error(),
        )

    def __call__(self, form, field):
        field_other = None
        for fld in form.fields:
            if fld.key == self.fieldname:
                field_other = fld
                break

        if not field_other:
            if callable(self.error_field_not_exists):
                error = self.error_field_not_exists()
            else:
                error = self.error_field_not_exists

            return error

        if field.value != field_other.value:
            return self.get_error()
