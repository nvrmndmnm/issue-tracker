# Generated by Django 3.2.7 on 2021-10-06 12:07

import django.core.validators
from django.db import migrations, models
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_alter_issue_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_started', models.DateField(verbose_name='Start date')),
                ('date_ended', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('name', models.CharField(max_length=150, validators=[webapp.models.MinValueValidator(5), django.core.validators.RegexValidator(message='Value should only contain Latin letters and numbers.', regex='^[ a-zA-Z0-9]*$')], verbose_name='Project name')),
                ('description', models.TextField(max_length=2000, verbose_name='Project description')),
            ],
        ),
    ]
