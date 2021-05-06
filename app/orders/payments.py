# encoding: utf-8
import os
import uuid
import pprint
import base64, hashlib
import json
import logging
from urllib.parse import urlparse
from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from users.models import CustomUser, Consultant
from orders.models import Package, PackageOrder


logging.getLogger("").setLevel(logging.DEBUG)

# SANDBOX = True
SANDBOX = False

LIQPAY_PUBLIC = os.environ.get("i6832340413"),
LIQPAY_PRIVATE = os.environ.get("XPBjSRkjee2ntkjtp9bkv0uHTUsK7ujAzpY7oRtR"),
BACK_URL = "%s://%s/pay-back/%s/"
VALID_STATUS = [
    "success",
]

DATASET = {
    "version": 3,
    "public_key": LIQPAY_PUBLIC,
    "private_key": LIQPAY_PRIVATE,
    "action": "pay",
    "amount": 1,
    "currency": "UAH",
    "description": None,
    "order_id": None,
    "paytypes": "card liqpay privat24 masterpass qr".split(),
}


class Order(object):
    def __init__(self, request, id):
        self.package = Package.objects.get(pk=id)
        self.user = request.user
        self.referrer = request.META.get("HTTP_REFERER")
        self.first_name = self.user.first_name
        self.second_name = self.user.second_name
        self.info = f"tel: {self.user.phone} e_mail: {self.user.email}"

    def _set_order_num(self):
        self.order_id = str(uuid.uuid1())

    def _set_order_name(self):
        params = dict(name=self.package.name, amount=self.package.amount)

    def _set_order_price(self):
        self.price = float(self.package.price)

    def _store_data(self):
        data = dict(user=self.user, referrer=self.referrer, package=self.package.pk,)

    def _pre_register(self):
        date_start = timezone.now()
        date_end = date_start + timedelta(days=self.package.duration)
        rec = dict(
            user=self.user,
            target=self.package,
            order_id=self.order_id,
            date_start=date_start,
            date_end=date_end,
            confirmed=False,
        )
        # logging.error(**rec)

        if not PackageOrder.objects.filter(order_id=self.order_id).exists():
            package_order = PackageOrder(**rec)
            package_order.save()

    def get_item(self):
        self._set_order_num()
        self._set_order_name()
        self._set_order_price()
        self._pre_register()
        self._store_data()
        return dict(
            order=self.order_id,
            name=self.package.name,
            price=self.price,
            first_name=self.first_name,
            second_name=self.second_name,
            info=self.info,
            referrer=self.referrer,
        )


class OrderRegister(object):
    def __init__(self, order_id):
        self.order_id = order_id

    def _validate_request(self, post):
        if SANDBOX:
            VALID_STATUS.append("sandbox")

        data = post["data"][0]

        signature = "{1}{0}{1}".format(data, LIQPAY_PRIVATE)
        joined_fields = joined_fields.encode("utf-8")
        signature = hashlib.sha1(signature).digest()
        signature = base64.b64encode(signature)
        if not signature == post["signature"][0]:
            logging.critical("Wrong signature %s", signature)
            return False

        data = base64.b64decode(data)
        data = json.loads(data)
        logging.debug("Validating data")
        logging.debug(data)

        if not data["public_key"] == LIQPAY_PUBLIC:
            logging.critical("Wrong public key %s", data["public_key"])
            return False
        if not data["status"] in VALID_STATUS:
            logging.critical(VALID_STATUS)
            logging.critical("Invalid status %s", data["status"])
            return False
        if not data["action"] == "pay":
            logging.critical("Invalid action %s", data["action"])
            return False
        data["liqpay_order_id"]
        logging.debug(data)
        return True

    def register(self):

        print(self.order_id)
        try:
            package_order = PackageOrder.objects.get(order_id=self.order_id)
        except:
            package_order = False

        if package_order:
            package_order.confirmed = True
            package_order.save()


class LiqPay(object):
    def __init__(self, order, name, price, first_name, second_name, info, referrer):
        scheme, netloc, _, _, _, _ = list(urlparse(referrer))
        data = dict(
            order_id=order,
            description=f"{name}",
            amount=price,
            sender_first_name=first_name,
            sender_second_name=second_name,
            info=info,
            result_url=referrer,
            server_url=BACK_URL % (scheme, netloc, order),
        )
        self.dataset = DATASET.copy()
        self.dataset.update(data)
        if SANDBOX:
            self.dataset.update(
                {"sandbox": 1,}
            )
            VALID_STATUS.append("sandbox")

        pprint.pprint(self.dataset)

    def _make_signature(self, *args):
        joined_fields = "".join(x for x in args)
        joined_fields = joined_fields.encode("utf-8")
        return base64.b64encode(hashlib.sha1(joined_fields).digest()).decode("ascii")

    def pack(self):

        json_encoded_data = json.dumps(self.dataset)
        signature = self._make_signature(
            LIQPAY_PRIVATE, json_encoded_data, LIQPAY_PRIVATE
        )

        # logging.error(signature)
        return json_encoded_data, signature


@login_required
def pay_package(request, id, slug=None):
    # logging.basicConfig( level=logging.DEBUG )
    # log = logging.getLogger("ex")
    # logging.debug("This is a debug message")
    # log.info("Informational message")
    # logging.error("An error has happened!")

    context = {}
    action = "https://www.liqpay.ua/api/3/checkout"
    template = "orders/pay_packages.html"
    order = Order(request, id)
    data = order.get_item()
    liqpay = LiqPay(**data)
    data, signature = liqpay.pack()
    context.update({"data": data, "signature": signature, "action": action})

    return render(request, template, context)


@csrf_exempt
def pay_back(request, order_id):
    # logging.basicConfig( level=logging.DEBUG, filename='payment.log' )

    order = OrderRegister(order_id)
    order.register()
    if request.method == "POST":
        post = dict(request.POST)
        logging.debug(order_id)
        print(post)

        order = OrderRegister(order_id)
        order.register()
        if order._validate_request(post):
            order.register()

    return HttpResponse()
