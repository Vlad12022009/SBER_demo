# Generated by Django 5.0.7 on 2024-08-04 08:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transition', '0003_remove_userprofile_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfermodel',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='transfermodel',
            name='read_status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.AddField(
            model_name='transfermodel',
            name='read_status_recipient',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='transfermodel',
            name='read_status_sender',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='transfermodel',
            name='commentary',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='money',
            field=models.IntegerField(default=10000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
