# Generated by Django 5.1.6 on 2025-07-02 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_remove_user_vinculo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='serie',
        ),
        migrations.RemoveField(
            model_name='user',
            name='turno',
        ),
        migrations.AddField(
            model_name='user',
            name='perfil',
            field=models.CharField(choices=[('aluno', 'Aluno'), ('administrador', 'Administrador'), ('monitor', 'Monitor')], default='aluno', max_length=20),
        ),
    ]
