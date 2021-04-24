# Generated by Django 3.2 on 2021-04-24 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('friendly_name', models.CharField(blank=True, max_length=254)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='none', max_length=254, null=True)),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True)),
                ('discounts', models.DecimalField(decimal_places=3, default=0.0, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=254)),
                ('name', models.CharField(default='new_product', max_length=254)),
                ('friendly_name', models.CharField(blank=True, max_length=254)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6)),
                ('rating', models.IntegerField(default=0)),
                ('number_of_ratings', models.IntegerField(blank=True, default=0, null=True)),
                ('rating_total', models.IntegerField(blank=True, default=0, null=True)),
                ('image_url_mobile', models.URLField(blank=True, max_length=1024)),
                ('image_url_desktop', models.URLField(blank=True, max_length=1024)),
                ('image_mobile', models.ImageField(blank=True, upload_to='')),
                ('image_desktop', models.ImageField(blank=True, max_length=1024, upload_to='')),
                ('digital_download', models.BooleanField(blank=True, default=False, null=True)),
                ('product_type', models.CharField(blank=True, max_length=254)),
                ('number_of_pictures', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
                ('special_offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.special')),
            ],
        ),
    ]