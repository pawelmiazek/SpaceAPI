# Generated by Django 3.2.9 on 2021-11-11 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Core",
            fields=[
                (
                    "id",
                    models.CharField(
                        editable=False, max_length=40, primary_key=True, serialize=False
                    ),
                ),
                (
                    "reuse_count",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="reuse count"
                    ),
                ),
                (
                    "payload",
                    models.PositiveSmallIntegerField(default=0, verbose_name="payload"),
                ),
            ],
            options={
                "verbose_name": "Core",
                "verbose_name_plural": "Cores",
            },
        ),
    ]