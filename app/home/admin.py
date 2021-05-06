from django.contrib import admin

# Register your models here.
from .models import Theme


class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
    )
    list_editable = ("order",)
    search_fields = [
        "name",
    ]


admin.site.register(Theme, ThemeAdmin)
