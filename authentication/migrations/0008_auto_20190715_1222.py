# Generated by Django 2.2.3 on 2019-07-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password1',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=121, max_length=20),
            preserve_default=False,
        ),
    ]
