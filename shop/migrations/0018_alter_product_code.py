# Generated by Django 3.2.5 on 2022-03-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]
