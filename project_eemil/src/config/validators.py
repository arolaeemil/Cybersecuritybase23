from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Your password must contain an uppercase letter (at least one)."),
                code='password_no_uppercase',
            )

    def get_help_text(self):
        return _(
            "Your password must contain an uppercase letter (at least one)."
        )