# Generated by Django 3.2.5 on 2022-03-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_order_complete_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]