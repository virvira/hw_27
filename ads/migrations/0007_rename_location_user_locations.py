# Generated by Django 4.1.5 on 2023-01-28 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_alter_user_options_remove_user_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='locations',
        ),
    ]
