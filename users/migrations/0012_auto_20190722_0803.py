# Generated by Django 2.2.3 on 2019-07-22 08:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='followee_id',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='followee_name',
        ),
        migrations.AddField(
            model_name='follower',
            name='followee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followees', to='users.User'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follower',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='users.User'),
        ),
    ]