# Generated by Django 2.2.9 on 2020-02-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="packageorder",
            name="order_id",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Liqpay"
            ),
        ),
    ]
