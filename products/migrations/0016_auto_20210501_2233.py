# Generated by Django 3.2 on 2021-05-01 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_product_qr_retrieval_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock_count',
            new_name='online_stock_count',
        ),
        migrations.AddField(
            model_name='product',
            name='store_stock_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='qr_retrieval_key',
            field=models.CharField(default='f79ba41b-efe4-40b6-908b-c6af549da192', max_length=254),
        ),
    ]
