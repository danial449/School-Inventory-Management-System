# Generated by Django 4.2.11 on 2024-04-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
