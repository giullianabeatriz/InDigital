# Generated by Django 5.1.6 on 2025-02-18 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indigital', '0012_alter_disponibilidade_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='disponibilidade',
            unique_together={('laboratorio', 'data', 'horario')},
        ),
    ]
