# Generated by Django 5.1.1 on 2024-10-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_plyuser_profile_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plyuser',
            name='uuid',
            field=models.UUIDField(default='072f7f', editable=False, unique=True),
        ),
    ]
