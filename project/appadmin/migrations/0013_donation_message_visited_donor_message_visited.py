# Generated by Django 5.0.3 on 2024-05-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0012_alter_customuser_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation_message',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donor_message',
            name='visited',
            field=models.BooleanField(default=False),
        ),
    ]
