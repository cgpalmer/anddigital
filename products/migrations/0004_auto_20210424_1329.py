# Generated by Django 3.2 on 2021-04-24 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210424_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qr_retrieval_key',
            field=models.CharField(default='05a4054f-daf2-4a21-b016-ec388894ee8d', max_length=254),
        ),
        migrations.AddField(
            model_name='product',
            name='qr_status',
            field=models.BooleanField(default=False),
        ),
    ]