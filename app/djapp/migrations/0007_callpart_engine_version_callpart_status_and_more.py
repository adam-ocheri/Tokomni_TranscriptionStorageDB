# Generated by Django 5.0.3 on 2024-03-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0006_delete_dbitem_callpart_callpart_uuid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='callpart',
            name='engine_version',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='callpart',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='callpart',
            name='callpart_uuid',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='callpart',
            name='extension_uuid',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='fullcalldata',
            name='calllog_uuid',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='fullcalldata',
            name='cdr_uuid',
            field=models.CharField(max_length=200),
        ),
    ]