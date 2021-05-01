# Generated by Django 3.2 on 2021-05-01 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service', '0002_alter_enquiry_enquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
                ('postcode', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
