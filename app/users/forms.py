from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        # Comma after field is needed
        fields = ("phone", "email")
        error_css_class = "uk-form-danger"

    # Making `email` a required field only during registration
    def __init__(self, *args, **kwargs):
        # call parent's constructor
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # setting `fields` property
        self.fields["email"].required = True
        self.fields["phone"].widget.attrs["type"] = "tel"
        self.fields["phone"].widget.attrs["placeholder"] = "+38(099)000-00-00"

    # Case insenstive email check
    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        email = cleaned_data.get("email")
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            self.add_error("email", "Користувач з таким email вже існує.")

        phone = cleaned_data.get("phone")
        if phone and CustomUser.objects.filter(phone__iexact=phone).exists():
            self.add_error("phone", "Користувач з таким телефоном вже існує.")

        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "phone",
            "email",
            "first_name",
            "second_name",
            "company_name",
            "company_edrpou",
            "company_ipn",
        )
        error_css_class = "uk-form-danger"

    def clean(self):
        cleaned_data = super(CustomUserChangeForm, self).clean()
        email = cleaned_data.get("email")
        if (
            email.lower() != self.instance.email.lower()
            and CustomUser.objects.filter(email__iexact=email).exists()
        ):
            self.add_error("email", "Користувач з таким email вже існує.")

        phone = cleaned_data.get("phone")
        if (
            phone.lower() != self.instance.phone.lower()
            and CustomUser.objects.filter(phone__iexact=phone).exists()
        ):
            self.add_error("phone", "Користувач з таким телефоном вже існує.")
        return cleaned_data


class CustomUserCreationFormPersonal(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        # Comma after field is needed
        fields = ("phone", "email", "first_name", "second_name", "terms_accepted")
        error_css_class = "uk-form-danger"

    # Making `email` a required field only during registration
    def __init__(self, *args, **kwargs):
        # call parent's constructor
        super(CustomUserCreationFormPersonal, self).__init__(*args, **kwargs)
        # setting `fields` property
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["second_name"].required = True
        self.fields["phone"].widget.attrs["type"] = "tel"
        self.fields["phone"].widget.attrs["autofocus"] = "false"
        self.fields["phone"].widget.attrs["placeholder"] = "+38(099)000-00-00"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Підтвердження пароля"
        self.fields["password1"].widget.attrs["type"] = "text"
        self.fields["password2"].widget.attrs["type"] = "text"
        self.fields[
            "terms_accepted"
        ].label = "З правилами користування сервісом погоджуюсь"

    # Case insenstive email check
    def clean(self):
        cleaned_data = super(CustomUserCreationFormPersonal, self).clean()

        terms_accepted = cleaned_data.get("terms_accepted")
        if terms_accepted is False:
            self.add_error(
                "terms_accepted",
                "Вам необхідно ознайомитись та погодитись з правилами користування сервісом",
            )

        email = cleaned_data.get("email")
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            self.add_error("email", "Користувач з таким email вже існує.")

        phone = cleaned_data.get("phone")
        if phone and CustomUser.objects.filter(phone__iexact=phone).exists():
            self.add_error("phone", "Користувач з таким телефоном вже існує.")

        if "+38(" not in phone:
            self.add_error("phone", "Перевірте правильність телефона")

        if len(phone) < 17:
            self.add_error("phone", "Перевірте правильність телефона")

        return cleaned_data


class CustomUserCreationFormCompany(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("company_name", "company_edrpou", "company_ipn")
        error_css_class = "uk-form-danger"

    def __init__(self, *args, **kwargs):
        # call parent's constructor
        super(CustomUserCreationFormCompany, self).__init__(*args, **kwargs)
        # setting `fields` property
        self.fields["company_name"].required = True
        self.fields["company_edrpou"].required = True

    target = forms.IntegerField(
        label="Обраний пакет", required=True, widget=forms.HiddenInput()
    )

    # def clean(self):
    #     cleaned_data = super(CustomUserCreationFormCompany, self).clean()
    #     email = cleaned_data.get('email')
    #     if email.lower() != self.instance.email.lower() and CustomUser.objects.filter(email__iexact=email).exists():
    #         self.add_error('email', 'Користувач з таким email вже існує.')

    #     phone = cleaned_data.get('phone')
    #     if phone.lower() != self.instance.phone.lower() and CustomUser.objects.filter(phone__iexact=phone).exists():
    #         self.add_error('phone', 'Користувач з таким телефоном вже існує.')
    #     return cleaned_data
