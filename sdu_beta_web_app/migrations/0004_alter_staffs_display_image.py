# Generated by Django 3.2 on 2021-05-03 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdu_beta_web_app', '0003_alter_staffs_display_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='display_image',
            field=models.FileField(upload_to=''),
        ),
    ]
