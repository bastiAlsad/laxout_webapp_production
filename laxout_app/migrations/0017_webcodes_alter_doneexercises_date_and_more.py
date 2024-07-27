# Generated by Django 5.0.2 on 2024-05-25 14:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("laxout_app", "0016_sovenduscustomeruid_alter_doneexercises_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebCodes",
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
                ("created_by", models.IntegerField(default=0)),
                ("code", models.CharField(default="", max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="doneexercises",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 25, 14, 49, 25, 890672)
            ),
        ),
        migrations.AlterField(
            model_name="doneworkouts",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 25, 14, 49, 25, 890150)
            ),
        ),
        migrations.AlterField(
            model_name="indexeslaxoutuser",
            name="creation_date",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="indexesphysios",
            name="for_month",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="indexesphysios",
            name="for_week",
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 5, 25, 14, 49, 25, 894407, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuser",
            name="last_meet",
            field=models.DateField(
                default=datetime.datetime(2024, 5, 25, 14, 49, 25, 894572)
            ),
        ),
        migrations.AlterField(
            model_name="laxoutuserindexcreationlog",
            name="for_month",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="laxoutuserindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name="laxoutuserpains",
            name="for_month",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="laxoutuserpains",
            name="for_week",
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name="physioindexcreationlog",
            name="for_month",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="physioindexcreationlog",
            name="for_week",
            field=models.IntegerField(default=21),
        ),
    ]
