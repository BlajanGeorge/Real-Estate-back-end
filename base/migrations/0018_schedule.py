# Generated by Django 4.2 on 2023-04-22 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_property_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.BigIntegerField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
    ]