import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon.entities.all():
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.image.url)
            )
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(pk=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    img_url = request.build_absolute_uri(requested_pokemon.image.url)
    for pokemon_entity in requested_pokemon.entities.all():
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )
    pokemon_info = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': img_url,
        'description': requested_pokemon.description,
    }
    if requested_pokemon.previous_evolution:
        parent = requested_pokemon.previous_evolution
        pokemon_info['previous_evolution'] = {
            'title_ru': parent.title,
            'pokemon_id': parent.id,
            'img_url': request.build_absolute_uri(parent.image.url)
        }
    next_evolution = requested_pokemon.next_evolutions.all()
    if next_evolution:
        child = next_evolution[0]
        pokemon_info['next_evolution'] = {
            'title_ru': child.title,
            'pokemon_id': child.id,
            'img_url': request.build_absolute_uri(child.image.url)
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
