# Generated by Django 5.0.6 on 2024-06-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appevaluacion', '0006_evaluacion_codigo_evaluacion_eliminado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
