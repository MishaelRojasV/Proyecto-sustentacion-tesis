# Generated by Django 5.0.7 on 2024-10-30 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appevaluacion', '0008_detalleevaluacion_jornada'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='estadoFinal',
            field=models.IntegerField(default=0),
        ),
    ]
