# Generated by Django 2.1.7 on 2020-06-29 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plant_exchange', '0004_auto_20200629_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plant_uploader', to=settings.AUTH_USER_MODEL),
        ),
    ]