# Generated by Django 5.0.7 on 2024-08-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appevaluacion', '0004_detalleevaluacion_alumno'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleevaluacion',
            name='estado',
            field=models.IntegerField(default=0),
        ),
    ]
