# Generated by Django 5.0.3 on 2024-04-07 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
