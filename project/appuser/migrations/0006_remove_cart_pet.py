# Generated by Django 5.0.3 on 2024-04-26 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0005_cart_adoptor_contact_cart_adoptor_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='pet',
        ),
    ]
