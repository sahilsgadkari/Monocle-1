from argparse import ArgumentParser
from datetime import datetime
from multiprocessing.managers import BaseManager, RemoteError
from time import time

from monocle import sanitized as conf
from monocle.db import get_forts, get_raids, Pokestop, session_scope, Sighting, Spawnpoint, Weather
from monocle.utils import Units, get_address
from monocle.names import DAMAGE, MOVES, POKEMON

import s2sphere

if conf.MAP_WORKERS:
    try:
        UNIT = getattr(Units, conf.SPEED_UNIT.lower())
        if UNIT is Units.miles:
            UNIT_STRING = "MPH"
        elif UNIT is Units.kilometers:
            UNIT_STRING = "KMH"
        elif UNIT is Units.meters:
            UNIT_STRING = "m/h"
    except AttributeError:
        UNIT_STRING = "MPH"

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-H',
        '--host',
        help='Set web server listening host',
        default='0.0.0.0'
    )
    parser.add_argument(
        '-P',
        '--port',
        type=int,
        help='Set web server listening port',
        default=5000
    )
    parser.add_argument(
        '-d', '--debug', help='Debug Mode', action='store_true'
    )
    parser.set_defaults(debug=False)
    return parser.parse_args()


class AccountManager(BaseManager): pass
AccountManager.register('worker_dict')


class Workers:
    def __init__(self):
        self._data = {}
        self._manager = AccountManager(address=get_address(), authkey=conf.AUTHKEY)

    def connect(self):
        try:
            self._manager.connect()
            self._data = self._manager.worker_dict()
        except (FileNotFoundError, AttributeError, RemoteError, ConnectionRefusedError, BrokenPipeError):
            print('Unable to connect to manager for worker data.')
            self._data = {}

    @property
    def data(self):
        try:
            if self._data:
                return self._data.items()
            else:
                raise ValueError
        except (FileNotFoundError, RemoteError, ConnectionRefusedError, ValueError, BrokenPipeError):
            self.connect()
            return self._data.items()


def get_worker_markers(workers):
    return [{
        'lat': lat,
        'lon': lon,
        'worker_no': worker_no,
        'time': datetime.fromtimestamp(timestamp).strftime('%I:%M:%S %p'),
        'speed': '{:.1f}{}'.format(speed, UNIT_STRING),
        'total_seen': total_seen,
        'visits': visits,
        'seen_here': seen_here
    } for worker_no, ((lat, lon), timestamp, speed, total_seen, visits, seen_here) in workers.data]


def sighting_to_marker(pokemon, names=POKEMON, moves=MOVES, damage=DAMAGE):
    pokemon_id = pokemon.pokemon_id
    marker = {
        'id': 'pokemon-' + str(pokemon.id),
        'trash': pokemon_id in conf.TRASH_IDS,
        'name': names[pokemon_id],
        'pokemon_id': pokemon_id,
        'lat': pokemon.lat,
        'lon': pokemon.lon,
        'expires_at': pokemon.expire_timestamp,
        'form': pokemon.form
    }
    move1 = pokemon.move_1
    if conf.MAP_SHOW_DETAILS and move1:
        move2 = pokemon.move_2
        marker['atk'] = pokemon.atk_iv
        marker['def'] = pokemon.def_iv
        marker['sta'] = pokemon.sta_iv
        marker['move1'] = moves[move1]
        marker['move2'] = moves[move2]
        marker['damage1'] = damage[move1]
        marker['damage2'] = damage[move2]
    return marker


def get_pokemarkers(after_id=0):
    with session_scope() as session:
        pokemons = session.query(Sighting) \
            .filter(Sighting.expire_timestamp > time(),
                    Sighting.id > after_id)
        if conf.MAP_FILTER_IDS:
            pokemons = pokemons.filter(~Sighting.pokemon_id.in_(conf.MAP_FILTER_IDS))
        return tuple(map(sighting_to_marker, pokemons))

def get_vertex(cell, v):
    vertex = s2sphere.LatLng.from_point(cell.get_vertex(v))
    return (vertex.lat().degrees, vertex.lng().degrees)

def get_weather():
    with session_scope() as session:
        weathers = session.query(Weather)
        markers = []
        for weather in weathers:
            cell = s2sphere.Cell(s2sphere.CellId(weather.s2_cell_id).parent(10))
            center = s2sphere.LatLng.from_point(cell.get_center())
            markers.append({
                'id': 'weather-' + str(weather.id),
                'coords': [(get_vertex(cell, v)) for v in range(0, 4)],
                'center': (center.lat().degrees, center.lng().degrees),
                'condition': weather.condition,
                'alert_severity': weather.alert_severity,
                'warn': weather.warn,
                'day': weather.day
            })
        return markers

def get_gym_markers(names=POKEMON):
    with session_scope() as session:
        forts = get_forts(session)
    return [{
            'id': 'fort-' + str(fort['fort_id']),
            'sighting_id': fort['id'],
            'gym_name': fort['name'],
            'image_url': fort['image_url'],
            'external_id': fort['external_id'],
            'pokemon_id': fort['guard_pokemon_id'],
            'pokemon_name': names[fort['guard_pokemon_id']],
            'is_in_battle': fort['is_in_battle'],
            'slots_available': fort['slots_available'],
            'time_occupied': fort['time_occupied'],
            'last_modified': fort['last_modified'],
            'team': fort['team'],
            'lat': fort['lat'],
            'lon': fort['lon']
    } for fort in forts]

def get_raid_markers(names=POKEMON, moves=MOVES):
    with session_scope() as session:
        raids = get_raids(session)
    return [{
            'id': 'raid-' + str(raid['fort_id']),
            'raid_id': raid['id'],
            'gym_name': raid['name'],
            'image_url': raid['image_url'],
            'external_id': raid['external_id'],
            'gym_team': raid['team'],
            'raid_battle': raid['raid_battle_ms'],
            'raid_spawn': raid['raid_spawn_ms'],
            'raid_end': raid['raid_end_ms'],
            'raid_level': raid['raid_level'],
            'raid_status': raid['complete'],
            'raid_pokemon_id': raid['pokemon_id'],
            'raid_pokemon_name': names[raid['pokemon_id']],
            'raid_pokemon_cp': raid['cp'],
            'raid_pokemon_move_1': moves[raid['move_1']],
            'raid_pokemon_move_2': moves[raid['move_2']],
            'lat': raid['lat'],
            'lon': raid['lon']
    } for raid in raids]

def get_spawnpoint_markers():
    with session_scope() as session:
        spawns = session.query(Spawnpoint)
        return [{
            'spawn_id': spawn.spawn_id,
            'despawn_time': spawn.despawn_time,
            'lat': spawn.lat,
            'lon': spawn.lon,
            'duration': spawn.duration
        } for spawn in spawns]

if conf.BOUNDARIES:
    from shapely.geometry import mapping

    def get_scan_coords():
        coordinates = mapping(conf.BOUNDARIES)['coordinates']
        coords = coordinates[0]
        markers = [{
                'type': 'scanarea',
                'coords': coords
            }]
        for blacklist in coordinates[1:]:
            markers.append({
                    'type': 'scanblacklist',
                    'coords': blacklist
                })
        return markers
else:
    def get_scan_coords():
        return ({
            'type': 'scanarea',
            'coords': (conf.MAP_START, (conf.MAP_START[0], conf.MAP_END[1]),
                       conf.MAP_END, (conf.MAP_END[0], conf.MAP_START[1]), conf.MAP_START)
        },)


def get_pokestop_markers():
    with session_scope() as session:
        pokestops = session.query(Pokestop)
        return [{
            'external_id': pokestop.external_id,
            'lat': pokestop.lat,
            'lon': pokestop.lon
        } for pokestop in pokestops]


def sighting_to_report_marker(sighting):
    return {
        'icon': 'static/monocle-icons/icons/{}.png'.format(sighting.pokemon_id),
        'lat': sighting.lat,
        'lon': sighting.lon,
    }

