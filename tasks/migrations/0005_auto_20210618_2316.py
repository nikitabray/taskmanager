# Generated by Django 3.2.4 on 2021-06-18 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20210618_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltask',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
