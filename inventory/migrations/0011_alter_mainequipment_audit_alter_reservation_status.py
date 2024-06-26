# Generated by Django 4.2.11 on 2024-04-23 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0010_alter_reservation_return_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainequipment",
            name="audit",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("Requested", "Requested"),
                    ("Reserved", "Reserved"),
                    ("Declined", "Declined"),
                    ("Returned", "Returned"),
                ],
                default="Requested",
                max_length=20,
            ),
        ),
    ]
