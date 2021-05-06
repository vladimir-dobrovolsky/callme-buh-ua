from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Телефон (phone) вместо username как основной идентификатор
    """

    def create_user(self, phone, password, **extra_fields):
        """
        Создание User с телефоном и паролем.
        """
        if not phone:
            raise ValueError(_("The phone must be set"))

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Создание SuperUser с телефоном и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)

    def get_by_natural_key(self, phone):
        case_insensitive_phone_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_phone_field: phone})
