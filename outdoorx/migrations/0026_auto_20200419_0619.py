# Generated by Django 3.0.4 on 2020-04-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outdoorx', '0025_location_location_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(default='../pic_folder/None/no-img.jpg', upload_to='../pic_folder'),
        ),
    ]
