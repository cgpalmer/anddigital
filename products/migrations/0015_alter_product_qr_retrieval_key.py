# Generated by Django 3.2 on 2021-05-01 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20210501_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='qr_retrieval_key',
            field=models.CharField(default='2e3e952f-8d8d-4968-98b0-0e1873875afc', max_length=254),
        ),
    ]