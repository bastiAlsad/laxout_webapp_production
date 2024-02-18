# Generated by Django 5.0 on 2024-02-11 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("laxout_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="First",
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
                ("first", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Second",
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
                ("second", models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name="doneexercises",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 11, 20, 2, 44, 888454)
            ),
        ),
        migrations.AlterField(
            model_name="doneworkouts",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 11, 20, 2, 44, 888020)
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 2, 11, 20, 2, 44, 892242, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="last_meet",
            field=models.DateField(
                default=datetime.datetime(2024, 2, 11, 20, 2, 44, 892395)
            ),
        ),
        migrations.CreateModel(
            name="Uebungen_Models",
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
                ("execution", models.CharField(default="", max_length=400)),
                ("name", models.CharField(default="", max_length=40)),
                ("dauer", models.IntegerField(default=30)),
                ("videoPath", models.CharField(default="", max_length=100)),
                ("looping", models.BooleanField(default=False)),
                ("added", models.BooleanField(default=False)),
                ("instruction", models.CharField(default="", max_length=200)),
                ("timer", models.BooleanField(default=False)),
                ("required", models.CharField(default="", max_length=50)),
                ("imagePath", models.CharField(default="", max_length=50)),
                ("appId", models.IntegerField(default=0)),
                ("onlineVideoPath", models.CharField(default="", max_length=220)),
                ("first", models.ManyToManyField(to="laxout_app.first")),
                ("second", models.ManyToManyField(to="laxout_app.second")),
            ],
        ),
    ]
