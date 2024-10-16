# Generated by Django 5.0 on 2024-10-14 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0006_ambulanceservice_petrolbunkservice_towingservice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulanceservice',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider'),
        ),
        migrations.AlterField(
            model_name='petrolbunkservice',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider'),
        ),
        migrations.AlterField(
            model_name='towingservice',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider'),
        ),
        migrations.AlterField(
            model_name='workshopservice',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadside_app.serviceprovider'),
        ),
    ]