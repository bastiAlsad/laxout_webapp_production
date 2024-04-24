# Generated by Django 5.0.2 on 2024-03-07 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "laxout_app",
            "0010_alter_doneexercises_date_alter_doneworkouts_date_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="AiExercise",
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
                ("exercise_id", models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name="doneexercises",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 3, 7, 18, 7, 22, 745532)
            ),
        ),
        migrations.AlterField(
            model_name="doneworkouts",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 3, 7, 18, 7, 22, 745051)
            ),
        ),
        migrations.AlterField(
            model_name="indexesphysios",
            name="for_week",
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 3, 7, 18, 7, 22, 749085, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="last_meet",
            field=models.DateField(
                default=datetime.datetime(2024, 3, 7, 18, 7, 22, 749234)
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuserindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="laxoutuserpains",
            name="for_week",
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="physioindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=10),
        ),
        migrations.CreateModel(
            name="AiTrainingData",
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
                ("illness", models.CharField(default="", max_length=200)),
                ("created_by", models.IntegerField(default=0)),
                ("created_for", models.IntegerField(default=0)),
                (
                    "related_exercises",
                    models.ManyToManyField(to="laxout_app.aiexercise"),
                ),
            ],
        ),
    ]
