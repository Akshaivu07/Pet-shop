# Generated by Django 5.0.3 on 2024-05-11 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdonor', '0006_alter_pet_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='disapproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pet',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]