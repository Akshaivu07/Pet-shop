# Generated by Django 5.0.3 on 2024-05-02 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0009_cart_donor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='visited',
            field=models.BooleanField(default=False),
        ),
    ]
