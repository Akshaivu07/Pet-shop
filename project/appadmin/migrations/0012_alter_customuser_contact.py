# Generated by Django 5.0.3 on 2024-05-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0011_message_visited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contact',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
