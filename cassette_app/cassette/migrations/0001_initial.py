# Generated by Django 5.1.1 on 2024-10-03 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_title', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.plyuser')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedPlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('singer', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('youtube_url', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('like', models.IntegerField(blank=True, null=True)),
                ('color', models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow'), ('purple', 'Purple'), ('black', 'Black'), ('white', 'White'), ('pink', 'Pink')], default='purple', max_length=10)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('playlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cassette.playlist')),
            ],
        ),
    ]
