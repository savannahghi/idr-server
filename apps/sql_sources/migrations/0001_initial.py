# Generated by Django 4.0.4 on 2022-05-30 00:24

import apps.core.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleSqlMetadata',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(help_text='The version of this metadata.', max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('extract_name', models.CharField(blank=True, max_length=200, null=True)),
                ('sql_query', models.TextField(help_text='The actual SQL statement to be run against a database to retrieve data. Should be a valid SQL DML statement for the target database.')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.core.models.AuditBaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='SourceVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source_version', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.core.models.AuditBaseManager()),
            ],
        ),
    ]
