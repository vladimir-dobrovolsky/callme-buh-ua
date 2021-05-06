from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser
from django.contrib.auth.models import Group

from orders.models import PackageOrder, UserCall

from core.views import context
from itertools import chain
import operator

# DRF
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from django.contrib import messages

# messages.debug(request, '%s SQL statements were executed.' % count)
# messages.info(request, 'Three credits remain in your account.')
# messages.success(request, 'Profile details updated.')
# messages.warning(request, 'Your account expires in three days.')
# messages.error(request, 'Document deleted.')


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        phone = self.request.POST["phone"]
        password = self.request.POST["password1"]
        # authenticate user then login
        user = authenticate(phone=phone, password=password)
        login(self.request, user)
        messages.success(
            self.request,
            "Реєстрація успішна",
            extra_tags="accountcreation uk-box-shadow-large",
        )
        # try redirection to previous page
        try:
            if context["last_url"]:
                return redirect(context["last_url"])
            else:
                return redirect("/")

        except:
            return redirect("/")


@login_required
def user_update(request):
    obj = get_object_or_404(CustomUser, phone=request.user.phone)
    template_name = "registration/profile.html"
    context["object"] = obj

    orders = PackageOrder.objects.filter(user=request.user)
    calls = UserCall.objects.filter(user=request.user)
    context["orders"] = orders
    context["calls"] = calls

    # Считаем количество доступных звонков по формуле
    # сумма купленных звонков (из всех подтвержденных действующих пакетов)
    # МИНУС сумма подтвержденных звонков на горячую линию за периоды действия пакетов

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

    available_calls = ordered_calls - calls_confirmed
    context["available_calls"] = available_calls
    context["currently_active_end_date"] = currently_active_end_date

    form = CustomUserChangeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Дані збережено",
            extra_tags="accountmodification uk-box-shadow-large",
        )

    context["form"] = form
    return render(request, template_name, context)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
