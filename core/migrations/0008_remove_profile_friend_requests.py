# Generated by Django 5.1.3 on 2024-12-02 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_profile_friend_requests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friend_requests',
        ),
    ]