from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect

try:
    from django.contrib.sites.models import Site
except:
    context["site_title"] = "Site import error in core views.py"

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.cache import cache_control

contacts = {"hotline": {"url": "tel:+380800502960", "number": "0-800-50-29-60"}}


context = {
    "contacts": contacts,
}

try:
    context["current_site"] = Site.objects.get_current()
    context["site_title"] = context["current_site"].name
except:
    print("Site object error in core views.py")
    # set title
    context["site_title"] = "Site title error in core views.py"
finally:
    pass


site_title = context["site_title"]

admin.site.site_header = context["site_title"]
admin.site.site_title = context["site_title"]


# @login_required


@cache_control(must_revalidate=True, max_age=3600)
def about_page(request):
    context["title"] = "Про нас" + " | " + site_title
    return render(request, "home/about.html", context)
