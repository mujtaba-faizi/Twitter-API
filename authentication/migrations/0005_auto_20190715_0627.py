# Generated by Django 2.2.3 on 2019-07-15 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
