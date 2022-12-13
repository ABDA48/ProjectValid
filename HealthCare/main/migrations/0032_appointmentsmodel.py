# Generated by Django 4.1.1 on 2022-10-27 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0031_remove_discussion_user_discussion_doctor_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppointmentsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("disease", models.CharField(max_length=20)),
                ("age", models.CharField(max_length=20)),
                ("slot", models.TimeField()),
                ("date", models.DateTimeField()),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.patientsmodel",
                    ),
                ),
            ],
        ),
    ]
