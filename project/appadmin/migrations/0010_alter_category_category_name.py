# Generated by Django 5.0.3 on 2024-04-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0009_remove_customuser_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='Category_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]