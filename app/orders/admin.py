from django.contrib import admin

# Register your models here.
from .models import Package, PackageOrder, UserCall


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
        "price",
    )
    list_editable = ("order",)
    search_fields = [
        "name",
    ]


class PackageOrderAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "user",
        "target",
        "targetprice",
        "date_start",
        "date_end",
        "confirmed",
    )
    list_editable = ("confirmed",)
    search_fields = [
        "user__phone",
        "user__email",
        "user__first_name",
        "user__second_name",
        "user__company_name",
        "user__company_edrpou",
        "user__company_ipn",
    ]
    autocomplete_fields = [
        "user",
    ]
    list_filter = [
        "confirmed",
        "target__name",
        "target__price",
    ]
    date_hierarchy = "created"


class UserCallAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "user",
        "answered_by",
        "topic",
        "confirmed",
    )
    list_editable = ("confirmed",)
    search_fields = [
        "user__phone",
        "user__email",
        "user__first_name",
        "user__second_name",
        "user__company_name",
        "user__company_edrpou",
        "user__company_ipn",
    ]
    list_filter = ["confirmed", "answered_by"]
    autocomplete_fields = ["user", "created_by", "answered_by", "topic"]
    date_hierarchy = "created"


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageOrder, PackageOrderAdmin)
admin.site.register(UserCall, UserCallAdmin)
