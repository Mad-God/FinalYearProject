# Generated by Django 3.2.5 on 2022-04-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_slide'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='shop/static/slides'),
        ),
    ]
