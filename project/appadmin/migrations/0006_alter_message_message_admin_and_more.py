# Generated by Django 5.0.3 on 2024-04-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appadmin', '0005_message_message_admin_message_message_doner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_admin',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_doner',
            field=models.TextField(default='', null=True),
        ),
    ]
