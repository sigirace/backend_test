# Generated by Django 4.1.7 on 2023-03-28 04:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='experience',
            name='perks',
            field=models.ManyToManyField(related_name='experiences', to='experiences.perk'),
        ),
    ]
