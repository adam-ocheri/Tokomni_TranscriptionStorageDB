# Generated by Django 5.0.3 on 2024-03-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0008_alter_callpart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callpart',
            name='callpart_uuid',
        ),
        migrations.AlterField(
            model_name='callpart',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
