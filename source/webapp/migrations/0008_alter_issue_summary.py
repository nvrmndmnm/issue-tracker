# Generated by Django 3.2.7 on 2021-09-30 09:42

import django.core.validators
from django.db import migrations, models
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_issue_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='summary',
            field=models.CharField(max_length=150, validators=[webapp.models.MinValueValidator(5), django.core.validators.RegexValidator(message='Value should only contain Latin letters and numbers.', regex='^[ a-zA-Z0-9]*$')], verbose_name='Summary'),
        ),
    ]
