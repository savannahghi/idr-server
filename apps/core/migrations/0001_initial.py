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
            name='GenericSource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.core.models.AuditBaseManager()),
            ],
        ),
    ]
