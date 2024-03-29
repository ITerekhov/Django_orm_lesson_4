# Generated by Django 3.1.14 on 2022-04-27 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_pokemon_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='parent',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon'),
        ),
    ]
