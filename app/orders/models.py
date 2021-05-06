from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

from users.models import CustomUser
from home.models import Theme

from datetime import datetime
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Package(models.Model):
    name = models.CharField("Назва пакета", max_length=50)
    duration = models.PositiveIntegerField(
        "Строк дії", null=True, blank=True, help_text="Скільки днів діє пакет"
    )
    amount = models.PositiveIntegerField(
        "Кількість дзвінків",
        null=True,
        blank=True,
        help_text="Скільки дзвінків містить пакет",
    )
    active = models.BooleanField(
        default=True, help_text="Чи доступний пакет для замовлення"
    )
    price = models.PositiveIntegerField(
        "Вартість",
        null=True,
        blank=True,
        help_text="Скільки коштує пакет (тільки цифра)",
    )
    description = models.TextField(null=True, blank=True, help_text="Опис пакета")
    order = models.IntegerField(
        "Порядок", null=True, blank=True, help_text="Порядок сортування"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["order"]
        verbose_name = "Пакет"
        verbose_name_plural = "Пакети"


class PackageOrder(models.Model):
    created = models.DateTimeField("Створено", auto_now_add=True,)
    target = models.ForeignKey(Package, on_delete=models.PROTECT, help_text="Пакет")
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, help_text="Замовник")

    date_start = models.DateField(
        "дата початку", blank=False, help_text="З якої дати активовано пакет"
    )
    date_end = models.DateField(
        "дата завершення", blank=False, help_text="До якої дати активовано пакет"
    )

    confirmed = models.BooleanField(
        "Підтверджено", blank=False, default=False, help_text="Оплату підтверджено"
    )
    order_id = models.CharField("Liqpay", max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def is_currently_active(self):
        if self.date_end < timezone.now() < self.date_start:
            return True
        else:
            return False

    def clean(self):
        date_delta = self.date_end - self.date_start
        if date_delta.days > self.target.duration:
            raise ValidationError("Встановлені дати перевищують строк дії пакета")

        if self.date_start > self.date_end:
            raise ValidationError("Дата початку пізніше за дату завершення")

        if not self.date_start.year >= 2020:
            raise ValidationError("Рік дати початку менший за 2020")

    def __str__(self):
        return f'{self.user} («{self.target}» з {self.date_start.strftime("%d.%m.%y")} по {self.date_end.strftime("%d.%m.%y")})'

    def targetprice(self):
        return f"{self.target.price} грн."


class UserCall(models.Model):
    created = models.DateTimeField("Створено", auto_now_add=True,)
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Клієнт",
        on_delete=models.PROTECT,
        help_text="Замовник",
        related_name="calls",
    )
    created_by = models.ForeignKey(
        CustomUser,
        verbose_name="Менеджер",
        on_delete=models.PROTECT,
        help_text="Менеджер",
        related_name="+",
        limit_choices_to=Q(groups__name="Менеджери"),
    )
    answered_by = models.ForeignKey(
        CustomUser,
        verbose_name="Фахівець",
        on_delete=models.PROTECT,
        help_text="Фахівець",
        related_name="answered_calls",
        limit_choices_to=Q(groups__name="Фахівці"),
    )
    topic = models.ForeignKey(
        Theme, verbose_name="Тема", on_delete=models.PROTECT, help_text="Тема"
    )
    confirmed = models.BooleanField(
        "Підтверджено", blank=False, default=False, help_text="Дзвінок зараховано"
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Дзвінок"
        verbose_name_plural = "Дзвінки"

    def __str__(self):
        return f"{self.created} -- {self.user} -> {self.answered_by}"
