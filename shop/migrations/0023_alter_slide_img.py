# Generated by Django 3.2.5 on 2022-04-16 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_slide_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='static/slides'),
        ),
    ]
