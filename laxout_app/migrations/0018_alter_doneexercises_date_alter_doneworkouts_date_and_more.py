# Generated by Django 5.0.2 on 2024-06-05 15:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("laxout_app", "0017_webcodes_alter_doneexercises_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doneexercises",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 6, 5, 15, 35, 53, 588513)
            ),
        ),
        migrations.AlterField(
            model_name="doneworkouts",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 6, 5, 15, 35, 53, 587820)
            ),
        ),
        migrations.AlterField(
            model_name="indexeslaxoutuser",
            name="creation_date",
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name="indexesphysios",
            name="for_month",
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name="indexesphysios",
            name="for_week",
            field=models.IntegerField(default=23),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 6, 5, 15, 35, 53, 593568, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="last_meet",
            field=models.DateField(
                default=datetime.datetime(2024, 6, 5, 15, 35, 53, 593778)
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuserindexcreationlog",
            name="for_month",
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name="laxoutuserindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=23),
        ),
        migrations.AlterField(
            model_name="laxoutuserpains",
            name="for_month",
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name="laxoutuserpains",
            name="for_week",
            field=models.IntegerField(default=23),
        ),
        migrations.AlterField(
            model_name="physioindexcreationlog",
            name="for_month",
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name="physioindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=23),
        ),
        migrations.CreateModel(
            name="AiTrainingDataGlobal",
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
                (
                    "related_exercises",
                    models.ManyToManyField(to="laxout_app.laxout_exercise"),
                ),
            ],
        ),
    ]
