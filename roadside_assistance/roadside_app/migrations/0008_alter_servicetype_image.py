# Generated by Django 5.1.2 on 2024-10-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0007_alter_servicetype_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='service_types/'),
        ),
    ]