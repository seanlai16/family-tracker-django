# Generated by Django 2.2.6 on 2019-10-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20191012_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geofence',
            name='radius',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]