# Generated by Django 3.2.4 on 2021-06-18 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210618_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicaltask',
            old_name='updated_at',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='updated_at',
            new_name='modified_at',
        ),
    ]