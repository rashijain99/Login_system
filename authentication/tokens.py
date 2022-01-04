from django.contrib.auth.tokens import PasswordResetTokenGenerator


# PasswordResetTokenGenerator is used to regenerate passwords, but we can use it to reactivate the account too.

from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )

generate_token = TokenGenerator()