# Generated by Django 4.2 on 2023-04-18 20:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('Romania', '+40'), ('USA', '+1'), ('Germany', '+49'), ('France', '+33'), ('Italy', '+39'), ('Brazil', '+55')], max_length=100)),
                ('city', models.CharField(choices=[('Bucuresti', 'Bucurest'), ('Cluj-Napoca', 'Cluj'), ('Brasov', 'Brasov'), ('Constanta', 'Constanta'), ('Timisoara', 'Timisoara'), ('New York', 'New York'), ('Los Angeles', 'Los Angeles'), ('Chicago', 'Chicago'), ('Munich', 'Munich'), ('Berlin', 'Berlin'), ('Frankfurt', 'Frankfurt'), ('Paris', 'Paris'), ('Lyon', 'Lyon'), ('Roma', 'Roma'), ('Napoli', 'Napoli'), ('Sao Paulo', 'Sao Paulo'), ('Rio de Janeiro', 'Rio De Janeiro')], max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('exchange', models.CharField(choices=[('Euro', 'Euro'), ('Dollar', 'Dollar'), ('Pound', 'Pound')], max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('square_feet', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(10)])),
                ('rooms', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)])),
                ('type', models.CharField(choices=[('House', 'House'), ('Apartment', 'Apartment')], max_length=20)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.propertyphoto')),
            ],
        ),
    ]
