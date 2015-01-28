from django.contrib.auth.models import User


def get_name_display(self):
    if self.first_name and self.last_name:
        return self.get_full_name()
    else:
        return self.get_username()

# We're monkey-patching the contrib.User model to reduce some boilerplate code
User.get_name_display = get_name_display

del(get_name_display)  # Don't need to pollutethe namespace
