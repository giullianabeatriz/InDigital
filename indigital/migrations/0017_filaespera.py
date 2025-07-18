# Generated by Django 5.1.6 on 2025-07-10 00:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indigital', '0016_remove_laboratorio_vagas_disponibilidade_vagas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FilaEspera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inscricao', models.DateTimeField(auto_now_add=True)),
                ('disponibilidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indigital.disponibilidade')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['data_inscricao'],
                'unique_together': {('usuario', 'disponibilidade')},
            },
        ),
    ]
