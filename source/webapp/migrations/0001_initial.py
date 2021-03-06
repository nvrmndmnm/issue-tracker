# Generated by Django 3.2.7 on 2021-09-16 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IssueStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Type')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=150, verbose_name='Summary')),
                ('description', models.CharField(max_length=2000, verbose_name='Description')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='statuses', to='webapp.issuestatus', verbose_name='Status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='types', to='webapp.issuetype', verbose_name='Type')),
            ],
        ),
    ]
