# Generated by Django 3.2.7 on 2021-10-21 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_project_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'permissions': [('superuser', 'All operations available')]},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('superuser', 'All operations available')]},
        ),
    ]
