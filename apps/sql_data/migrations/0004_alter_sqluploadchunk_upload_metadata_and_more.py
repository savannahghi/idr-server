# Generated by Django 4.2 on 2023-04-03 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sql_data", "0003_remove_sqluploadchunk_finish_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sqluploadchunk",
            name="upload_metadata",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="upload_chunks",
                to="sql_data.sqluploadmetadata",
            ),
        ),
        migrations.AlterField(
            model_name="sqluploadmetadata",
            name="extract_metadata",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="uploads",
                to="sql_data.sqlextractmetadata",
            ),
        ),
    ]
