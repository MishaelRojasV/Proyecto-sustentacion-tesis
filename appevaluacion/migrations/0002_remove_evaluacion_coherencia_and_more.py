# Generated by Django 5.0.7 on 2024-07-29 15:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appevaluacion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluacion',
            name='Coherencia',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='Dominio_tema',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='Importancia',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='Metodologia',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='Originalidad',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='Validez',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='jurado',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='puntajeFinal',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='sugerencias',
        ),
        migrations.AddField(
            model_name='alumno',
            name='ncelular',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='codigo',
            field=models.CharField(default=True, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jurado',
            name='dni',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='jurado',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jurado',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jurado',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jurado',
            name='telefono',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='jurado',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appevaluacion.alumno', unique=True),
        ),
        migrations.CreateModel(
            name='DetalleEvaluacion',
            fields=[
                ('idDetEvaluacion', models.AutoField(primary_key=True, serialize=False)),
                ('originalidad', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('importancia', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('coherencia', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('metodologia', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('validez', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('dominio_tema', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('puntajeFinal', models.IntegerField(default=0)),
                ('sugerencias', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('eliminado', models.BooleanField(default=False)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appevaluacion.alumno')),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appevaluacion.evaluacion')),
                ('jurado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appevaluacion.jurado')),
            ],
        ),
    ]
