from django.db import models

# Create your models here.


class Theme(models.Model):
    name = models.CharField("Назва", max_length=50)
    is_active = models.BooleanField(default=True, help_text="Чи активна тема")
    order = models.IntegerField(
        "Порядок", null=True, blank=True, help_text="Порядок сортування"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Тема"
        verbose_name_plural = "Теми"
