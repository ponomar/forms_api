import re

from forms_api.validators.regex_validator import RegexValidator


class EmailValidator(RegexValidator):
    def __init__(self, error=None):
        super().__init__(
            regex=(
                r'^[a-z0-9\-\_\.]+'
                r'@'
                r'[a-z0-9\-\_\.]*'  # text with multiple dots
                r'[a-z0-9]{1}'      # last not-dot symbol before dot
                r'\.'
                r'[a-z]{2,10}$'
            ),
            flags=re.IGNORECASE,
            error=error or 'Email is not valid.',
        )
