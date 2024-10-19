# Generated by Django 5.1.2 on 2024-10-19 06:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0002_servicetype_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbulanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FuelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TowingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AmbulanceService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider')),
                ('ambulance_types', models.ManyToManyField(to='roadside_app.ambulancetype')),
            ],
        ),
        migrations.CreateModel(
            name='PetrolBunkService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_types', models.ManyToManyField(to='roadside_app.fueltype')),
                ('service_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='TowingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider')),
                ('towing_types', models.ManyToManyField(to='roadside_app.towingtype')),
                ('vehicles', models.ManyToManyField(to='roadside_app.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider')),
                ('services', models.ManyToManyField(to='roadside_app.workshopservice')),
            ],
        ),
    ]
