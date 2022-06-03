# Generated by Django 3.2.5 on 2022-05-28 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_shop_phone'),
        ('shop', '0031_alter_category_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'shop')},
        ),
        migrations.AlterUniqueTogether(
            name='supplier',
            unique_together={('name', 'shop')},
        ),
    ]
