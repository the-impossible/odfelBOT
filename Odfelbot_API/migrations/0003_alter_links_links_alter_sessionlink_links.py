# Generated by Django 5.0.4 on 2024-05-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Odfelbot_API", "0002_announcement_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="links", name="links", field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name="sessionlink",
            name="links",
            field=models.URLField(max_length=500),
        ),
    ]
