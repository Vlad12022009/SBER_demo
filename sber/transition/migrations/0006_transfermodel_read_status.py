# Generated by Django 5.0.7 on 2024-08-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transition', '0005_remove_transfermodel_read_status_recipient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfermodel',
            name='read_status',
            field=models.BooleanField(default=False),
        ),
    ]
