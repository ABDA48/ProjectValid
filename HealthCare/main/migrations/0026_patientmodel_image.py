# Generated by Django 4.1.1 on 2022-10-26 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0025_remove_patientmodel_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="patientmodel",
            name="image",
            field=models.FileField(default="", upload_to="images/"),
        ),
    ]
