# Generated by Django 5.1.1 on 2024-09-30 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="family",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="name",
        ),
    ]
