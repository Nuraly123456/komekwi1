# Generated by Django 5.2 on 2025-05-04 08:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
