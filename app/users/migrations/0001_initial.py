# Generated by Django 2.2.9 on 2020-02-12 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=17, unique=True, verbose_name="контактний телефон"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="ім'я"
                    ),
                ),
                (
                    "second_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="прізвище"
                    ),
                ),
                ("terms_accepted", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="компанія"
                    ),
                ),
                (
                    "company_edrpou",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="ЄДРПОУ"
                    ),
                ),
                (
                    "company_ipn",
                    models.CharField(
                        blank=True, max_length=12, null=True, verbose_name="ІПН"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Користувач",
                "verbose_name_plural": "Користувачі",
                "ordering": ["-date_joined"],
            },
        ),
        migrations.CreateModel(
            name="Consultant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50, verbose_name="ім'я")),
                (
                    "second_name",
                    models.CharField(max_length=50, verbose_name="прізвище"),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "lector_photo",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True,
                        null=True,
                        upload_to=users.models.Consultant.photo_upload_path,
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        blank=True,
                        help_text="Порядок сортування",
                        null=True,
                        verbose_name="Порядок",
                    ),
                ),
                (
                    "c_user",
                    models.ForeignKey(
                        blank=True,
                        help_text="Пов`язаний обліковий запис користувача",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Фахівець",
                "verbose_name_plural": "Фахівці",
                "ordering": ["second_name"],
            },
        ),
    ]
