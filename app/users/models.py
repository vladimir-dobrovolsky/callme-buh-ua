from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from django.template import defaultfilters
from unidecode import unidecode

from .managers import CustomUserManager

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from home.models import Theme

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Для всех
    phone = models.CharField("контактний телефон", max_length=17, unique=True)
    email = models.EmailField("email", unique=True)
    first_name = models.CharField("ім'я", max_length=50, null=True, blank=True)
    second_name = models.CharField("прізвище", max_length=50, null=True, blank=True)
    terms_accepted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Для корпоративных, обязательность полей Компания и ЕГРПОУ регулируется в формах
    company_name = models.CharField("компанія", max_length=50, null=True, blank=True)
    company_edrpou = models.CharField("ЄДРПОУ", max_length=10, null=True, blank=True)
    company_ipn = models.CharField("ІПН", max_length=12, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        if self.is_staff:
            return f"{self.second_name} {self.first_name}"
        else:
            if self.company_name:
                return f"{self.company_name} {self.first_name} {self.phone}"
            else:
                return f"{self.phone} {self.first_name}"


class Consultant(models.Model):
    def photo_upload_path(self, filename):
        filename = filename.split(".")
        ext = filename[-1]
        filename = "%s.%s" % (defaultfilters.slugify(unidecode(self.second_name)), ext)
        return f"consultant_photos/{filename}"

    c_user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        help_text="Пов`язаний обліковий запис користувача",
        null=True,
        blank=True,
    )
    first_name = models.CharField("ім'я", max_length=50)
    second_name = models.CharField("прізвище", max_length=50)
    description = models.TextField(null=True, blank=True)
    lector_photo = ProcessedImageField(
        upload_to=photo_upload_path,
        processors=[ResizeToFit(512, 512)],
        format="JPEG",
        options={"quality": 95},
        null=True,
        blank=True,
    )
    order = models.IntegerField(
        "Порядок", null=True, blank=True, help_text="Порядок сортування"
    )

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        ordering = ["second_name"]
        verbose_name = "Фахівець"
        verbose_name_plural = "Фахівці"
