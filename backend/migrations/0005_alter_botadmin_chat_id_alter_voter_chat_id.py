# Generated by Django 5.0.6 on 2024-07-19 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_required_channels_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botadmin',
            name='chat_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='chat_id',
            field=models.BigIntegerField(),
        ),
    ]
