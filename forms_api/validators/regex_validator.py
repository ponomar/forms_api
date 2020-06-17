import re

from forms_api.validators.base_validator import Validator


class RegexValidator(Validator):
    def __init__(self, regex, flags=0, error=None, regex_js=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex
        self.regex_js = regex_js
        self.error = error

    def schema(self):
        result = dict(
            type='regex',
            regex=self.regex.pattern,
            error=self.get_error(),
        )
        if self.regex_js:
            result['regex_js'] = self.regex_js

        return result

    def __call__(self, form, field):
        if field.value is None and field.required is False:
            return

        if not self.regex.match(field.value or ''):
            return self.get_error()
