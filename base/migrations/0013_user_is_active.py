# Generated by Django 4.2 on 2023-04-19 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
