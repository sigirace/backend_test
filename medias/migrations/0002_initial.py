# Generated by Django 4.1.7 on 2023-03-31 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medias', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.room'),
        ),
    ]
