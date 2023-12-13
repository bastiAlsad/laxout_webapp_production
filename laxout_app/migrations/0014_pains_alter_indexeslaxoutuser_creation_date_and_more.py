# Generated by Django 5.0 on 2023-12-13 18:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laxout_app', '0013_coupon_alter_indexeslaxoutuser_creation_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paint_amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='indexeslaxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 13, 18, 28, 39, 776584, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='indexesphysios',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 13, 18, 28, 39, 776584, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 13, 18, 28, 39, 778584, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='laxoutuser',
            name='user_uid',
            field=models.CharField(default='8f536962-e438-4a2d-9a08-5d7e9151d34b', max_length=420, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='average_pain',
            field=models.ManyToManyField(to='laxout_app.pains'),
        ),
    ]
