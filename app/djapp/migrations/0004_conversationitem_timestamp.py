# Generated by Django 5.0.3 on 2024-03-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0003_alter_fullcalldata_callog_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationitem',
            name='timestamp',
            field=models.FloatField(default=0.0),
        ),
    ]
