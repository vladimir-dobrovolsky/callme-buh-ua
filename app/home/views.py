from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.views import context

from django.utils import timezone
from django.utils.dateformat import DateFormat

from django.contrib.auth import authenticate, login
from django.contrib import messages

from users.forms import CustomUserCreationFormPersonal, CustomUserCreationFormCompany
from users.models import CustomUser, Consultant
from home.models import Theme
from orders.models import Package, PackageOrder

# Для счета в xlsx
import os
from django.conf import settings
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from num2words import num2words


def home_page(request):

    # context["is_pc"]= request.user_agent.is_pc
    # context["is_mobile"]= request.user_agent.is_mobile
    context["home_consultants"] = Consultant.objects.all().order_by("order")
    context["home_themes"] = Theme.objects.filter(is_active=True).order_by(
        "order", "name"
    )

    # Показываем только активные пакеты
    context["home_packages"] = Package.objects.filter(active=True).order_by(
        "order", "name"
    )
    # context["home_packages"] = Package.objects.order_by('order', 'name')

    # Если пользователь не авторизовался, показываем форму регистрации с личными данными (первая колонка)
    if not request.user.is_authenticated:
        form = CustomUserCreationFormPersonal(request.POST or None)
        if form.is_valid():
            form.save()
            phone = request.POST["phone"]
            password = request.POST["password1"]
            # authenticate user then login
            user = authenticate(phone=phone, password=password)
            login(request, user)
            messages.success(
                request,
                "Реєстрація успішна",
                extra_tags="accountcreation uk-box-shadow-large",
            )
            return redirect("/#home-reg")

    # если же пользователь авторизован, показываем кнопку заказа через ликпей и форму для ввода данных компании (вторая колонка)
    else:
        user_to_update = get_object_or_404(CustomUser, id=request.user.id)
        form_prefill = {}
        if request.user.company_name:
            form_prefill["company_name"] = request.user.company_name
        if request.user.company_edrpou:
            form_prefill["company_edrpou"] = request.user.company_edrpou
        if request.user.company_ipn:
            form_prefill["company_ipn"] = request.user.company_ipn

        form_prefill["target"] = 1

        form = CustomUserCreationFormCompany(
            request.POST or None, instance=user_to_update, initial=form_prefill
        )
        if form.is_valid():
            data = form.cleaned_data
            form.save()

            try:
                target = Package.objects.get(id=data["target"])
                # Формируем заказ (счет) из шаблона в xlsx
                invoice_template = os.path.join(
                    settings.BASE_DIR, "www/media/invoice/invoice_template.xlsx"
                )
                wb = load_workbook(filename=invoice_template)
                ws1 = wb.active
                ws1.title = "Замовлення"
                dt = timezone.now()
                df = DateFormat(dt)

                price = target.price

                ws1["B5"] = f"від {df.format('d E Y')}р."
                ws1["G18"] = f"{data['company_name']}"
                ws1["O19"] = data["company_edrpou"]
                ws1["AB19"] = data["company_ipn"]
                ws1["AF26"] = f"{price}.00"
                ws1["AI26"] = f"{price}.00"
                ws1["AI28"] = f"{price}.00"
                tax = int(price / 6)
                tax_words = num2words(tax, lang="uk")
                price_words = num2words(price, lang="uk")
                ws1["AI29"] = f"{tax}.00"
                ws1["B31"] = f"Всього найменувань 1, на суму {price},00 грн."
                ws1["B32"] = f"{price_words} гривень 00 копійок"
                ws1["B33"] = f"У т.ч. ПДВ: {tax_words} гривень 00 копійок"

                response = HttpResponse(
                    save_virtual_workbook(wb), content_type="application/vnd.ms-excel"
                )
                response[
                    "Content-Disposition"
                ] = f'''attachment; filename="order-{df.format('d-m-Y')}.xlsx"'''

                # Пробуем создать запись о заказе перед тем как отправить пользователю файл счета
                try:
                    new_order_date_start = str(timezone.now().date())
                    new_order_date_end = str(
                        timezone.now().date() + timezone.timedelta(days=target.duration)
                    )

                    new_order = PackageOrder.objects.create(
                        target=target,
                        user=request.user,
                        date_start=new_order_date_start,
                        date_end=new_order_date_end,
                    )
                    new_order.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Замовлення створено",
                        extra_tags="uk-box-shadow-large",
                    )
                except:
                    pass

                return response

            except:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Помилка формування рахунку",
                    extra_tags="uk-box-shadow-large",
                )
                return redirect("/#home-reg")

    context["form"] = form

    return render(request, "home/index.html", context)
