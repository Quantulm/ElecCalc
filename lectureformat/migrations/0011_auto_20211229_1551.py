# Generated by Django 3.2 on 2021-12-29 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lectureformat", "0010_auto_20211229_1443"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturehall",
            name="university",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lectureformat.university",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="university",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lectureformat.university",
            ),
        ),
    ]
