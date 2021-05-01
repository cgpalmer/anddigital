# Generated by Django 3.2 on 2021-05-01 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20210501_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='number_of_pictures',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AlterField(
            model_name='product',
            name='qr_retrieval_key',
            field=models.CharField(default='f579e3e2-7363-483e-abff-a4f05a62d5f6', max_length=254),
        ),
    ]
