# Generated by Django 5.1 on 2024-09-14 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0004_rating"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="rating",
            name="unique_report_user_rating",
        ),
    ]
