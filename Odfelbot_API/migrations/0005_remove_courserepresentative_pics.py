# Generated by Django 5.0.4 on 2024-05-07 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Odfelbot_API", "0004_links_course"),
    ]

    operations = [
        migrations.RemoveField(model_name="courserepresentative", name="pics",),
    ]
