from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Consultant
from orders.models import PackageOrder, UserCall

from import_export.admin import ExportMixin
from import_export import resources

from django.utils import timezone


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        skip_unchanged = True
        report_skipped = True


class CustomUserAdmin(ExportMixin, UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def available_calls(self, obj=None):
        orders = PackageOrder.objects.filter(user=obj)
        calls = UserCall.objects.filter(user=obj)
        ordered_calls = 0
        now = timezone.now()
        currently_active_start_date = now.date()
        currently_active_end_date = now.date()
        orders_confirmed = orders.filter(
            confirmed=True, date_start__lte=now, date_end__gte=now
        )
        for entry in orders_confirmed:
            if entry.date_start < currently_active_start_date:
                currently_active_start_date = entry.date_start

            if entry.date_end > currently_active_end_date:
                currently_active_end_date = entry.date_end

            ordered_calls += entry.target.amount
        calls_confirmed = calls.filter(
            confirmed=True,
            created__range=(currently_active_start_date, currently_active_end_date),
        ).count()
        output = ordered_calls - calls_confirmed
        return format_html(
            "<a href='/admin/orders/usercall/?user__id__exact={id}'>{count}</a>",
            id=obj.id,
            count=output,
        )

    def used_calls(self, obj=None):
        calls = UserCall.objects.filter(user=obj)
        calls_confirmed = calls.filter(confirmed=True).count()
        output = calls_confirmed
        return format_html(
            "<a href='/admin/orders/usercall/?user__id__exact={id}'>{count}</a>",
            id=obj.id,
            count=calls_confirmed,
        )

    def had_orders(self, obj=None):
        orders = PackageOrder.objects.filter(user=obj)
        if orders:
            return format_html(
                "<a href='/admin/orders/packageorder/?user__id__exact={id}'>✔</a>",
                id=obj.id,
            )
        else:
            return "✕"

    used_calls.short_description = "Використано"
    available_calls.short_description = "Доступно"
    had_orders.short_description = "Замовляв"

    list_display = (
        "phone",
        "company_name",
        "used_calls",
        "available_calls",
        "had_orders",
        "first_name",
        "email",
        "is_staff",
        "date_joined",
    )
    list_filter = (
        "date_joined",
        "groups",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("phone", "email", "first_name", "second_name")}),
        ("Company", {"fields": ("company_name", "company_edrpou", "company_ipn")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = (
        "phone",
        "email",
        "company_name",
        "company_edrpou",
        "company_ipn",
        "first_name",
        "second_name",
    )
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions")
    resource_class = CustomUserResource


class ConsultantAdmin(admin.ModelAdmin):
    list_display = (
        "second_name",
        "first_name",
        "order",
    )
    list_editable = ("order",)
    search_fields = ["first_name", "second_name"]
    autocomplete_fields = [
        "c_user",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Consultant, ConsultantAdmin)
