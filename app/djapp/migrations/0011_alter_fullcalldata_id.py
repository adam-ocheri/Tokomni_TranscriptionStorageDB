# Generated by Django 5.0.3 on 2024-03-24 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0010_remove_fullcalldata_calllog_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullcalldata',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
