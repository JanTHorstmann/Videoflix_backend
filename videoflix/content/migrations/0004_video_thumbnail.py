# Generated by Django 5.1.1 on 2024-10-22 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_video_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='img'),
        ),
    ]
