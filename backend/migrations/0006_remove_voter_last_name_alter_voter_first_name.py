# Generated by Django 5.0.6 on 2024-07-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_botadmin_chat_id_alter_voter_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='voter',
            name='first_name',
            field=models.CharField(blank=True, max_length=1050),
        ),
    ]
