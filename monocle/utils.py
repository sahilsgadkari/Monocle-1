import socket

from os import mkdir
from os.path import join, exists
from sys import platform
from asyncio import sleep
from math import sqrt
from uuid import uuid4
from enum import Enum
from csv import DictReader
from cyrandom import choice, shuffle, uniform
from time import time
from pickle import dump as pickle_dump, load as pickle_load, HIGHEST_PROTOCOL

from geopy import Point
from geopy.distance import distance
from aiopogo import utilities as pgoapi_utils
from pogeo import get_distance

from . import bounds, sanitized as conf


IPHONES = {'iPhone5,1': 'N41AP',
           'iPhone5,2': 'N42AP',
           'iPhone5,3': 'N48AP',
           'iPhone5,4': 'N49AP',
           'iPhone6,1': 'N51AP',
           'iPhone6,2': 'N53AP',
           'iPhone7,1': 'N56AP',
           'iPhone7,2': 'N61AP',
           'iPhone8,1': 'N71AP',
           'iPhone8,2': 'N66AP',
           'iPhone8,4': 'N69AP',
           'iPhone9,1': 'D10AP',
           'iPhone9,2': 'D11AP',
           'iPhone9,3': 'D101AP',
           'iPhone9,4': 'D111AP'}


class Units(Enum):
    miles = 1
    kilometers = 2
    meters = 3


def best_factors(n):
    return next(((i, n//i) for i in range(int(n**0.5), 0, -1) if n % i == 0))


def percentage_split(seq, percentages):
    percentages[-1] += 1.0 - sum(percentages)
    prv = 0
    size = len(seq)
    cum_percentage = 0
    for p in percentages:
        cum_percentage += p
        nxt = int(cum_percentage * size)
        yield seq[prv:nxt]
        prv = nxt


def get_start_coords(worker_no, grid=conf.GRID, bounds=bounds):
    """Returns center of square for given worker"""
    per_column = int((grid[0] * grid[1]) / grid[0])

    column = worker_no % per_column
    row = int(worker_no / per_column)
    part_lat = (bounds.south - bounds.north) / grid[0]
    part_lon = (bounds.east - bounds.west) / grid[1]
    start_lat = bounds.north + part_lat * row + part_lat / 2
    start_lon = bounds.west + part_lon * column + part_lon / 2
    return start_lat, start_lon


def float_range(start, end, step):
    """range for floats, also capable of iterating backwards"""
    if start > end:
        while end <= start:
            yield start
            start += -step
    else:
        while start <= end:
            yield start
            start += step


def get_gains(dist=70):
    """Returns lat and lon gain

    Gain is space between circles.
    """
    start = Point(*bounds.center)
    base = dist * sqrt(3)
    height = base * sqrt(3) / 2
    dis_a = distance(meters=base)
    dis_h = distance(meters=height)
    lon_gain = dis_a.destination(point=start, bearing=90).longitude
    lat_gain = dis_h.destination(point=start, bearing=0).latitude
    return abs(start.latitude - lat_gain), abs(start.longitude - lon_gain)


def round_coords(point, precision, _round=round):
    return _round(point[0], precision), _round(point[1], precision)


def get_bootstrap_points(bounds):
    coords = []
    if bounds.multi:
        for b in bounds.polygons:
            coords.extend(get_bootstrap_points(b))
        return coords
    lat_gain, lon_gain = get_gains(conf.BOOTSTRAP_RADIUS)
    west, east = bounds.west, bounds.east
    bound = bool(bounds)
    for map_row, lat in enumerate(
        float_range(bounds.south, bounds.north, lat_gain)
    ):
        row_start_lon = west
        if map_row % 2 != 0:
            row_start_lon -= 0.5 * lon_gain
        for lon in float_range(row_start_lon, east, lon_gain):
            point = lat, lon
            if not bound or point in bounds:
                coords.append(point)
    shuffle(coords)
    return coords


def get_device_info(account):
    device_info = {'brand': 'Apple',
                   'device': 'iPhone',
                   'manufacturer': 'Apple'}
    try:
        if account['iOS'].startswith('1'):
            device_info['product'] = 'iOS'
        else:
            device_info['product'] = 'iPhone OS'
        device_info['hardware'] = account['model'] + '\x00'
        device_info['model'] = IPHONES[account['model']] + '\x00'
    except (KeyError, AttributeError):
        account = generate_device_info(account)
        return get_device_info(account)
    device_info['version'] = account['iOS']
    device_info['device_id'] = account['id']
    return device_info


def generate_device_info(account):
    ios9 = ('9.0', '9.0.1', '9.0.2', '9.1', '9.2', '9.2.1', '9.3', '9.3.1', '9.3.2', '9.3.3', '9.3.4', '9.3.5')
    # 10.0 was only for iPhone 7 and 7 Plus, and is rare
    ios10 = ('10.0.1', '10.0.2', '10.0.3', '10.1', '10.1.1', '10.2', '10.2.1', '10.3', '10.3.1', '10.3.2', '10.3.3')

    devices = tuple(IPHONES.keys())
    account['model'] = choice(devices)

    account['id'] = uuid4().hex

    if account['model'] in ('iPhone9,1', 'iPhone9,2',
                            'iPhone9,3', 'iPhone9,4'):
        account['iOS'] = choice(ios10)
    elif account['model'] in ('iPhone8,1', 'iPhone8,2'):
        account['iOS'] = choice(ios9 + ios10)
    elif account['model'] == 'iPhone8,4':
        # iPhone SE started on 9.3
        account['iOS'] = choice(('9.3', '9.3.1', '9.3.2', '9.3.3', '9.3.4', '9.3.5') + ios10)
    else:
        account['iOS'] = choice(ios9 + ios10)

    return account


def create_account_dict(account):
    if isinstance(account, (tuple, list)):
        length = len(account)
    else:
        raise TypeError('Account must be a tuple or list.')

    if length not in (1, 3, 4, 6):
        raise ValueError('Each account should have either 3 (account info only) or 6 values (account and device info).')
    if length in (1, 4) and (not conf.PASS or not conf.PROVIDER):
        raise ValueError('No default PASS or PROVIDER are set.')

    entry = {}
    entry['username'] = account[0]

    if length == 1 or length == 4:
        entry['password'], entry['provider'] = conf.PASS, conf.PROVIDER
    else:
        entry['password'], entry['provider'] = account[1:3]

    if length == 4 or length == 6:
        entry['model'], entry['iOS'], entry['id'] = account[-3:]
    else:
        entry = generate_device_info(entry)

    entry['time'] = 0
    entry['captcha'] = False
    entry['banned'] = False

    return entry


def accounts_from_config(pickled_accounts=None):
    accounts = {}
    for account in conf.ACCOUNTS:
        username = account[0]
        if pickled_accounts and username in pickled_accounts:
            accounts[username] = pickled_accounts[username]
            if len(account) == 3 or len(account) == 6:
                accounts[username]['password'] = account[1]
                accounts[username]['provider'] = account[2]
        else:
            accounts[username] = create_account_dict(account)
    return accounts


def accounts_from_csv(new_accounts, pickled_accounts):
    accounts = {}
    for username, account in new_accounts.items():
        if pickled_accounts:
            pickled_account = pickled_accounts.get(username)
            if pickled_account:
                if pickled_account['password'] != account['password']:
                    del pickled_account['password']
                account.update(pickled_account)
            accounts[username] = account
            continue
        account['provider'] = account.get('provider') or 'ptc'
        if not all(account.get(x) for x in ('model', 'iOS', 'id')):
            account = generate_device_info(account)
        account['time'] = 0
        account['captcha'] = False
        account['banned'] = False
        accounts[username] = account
    return accounts


def get_current_hour(now=None, _time=time):
    now = now or _time()
    return round(now - (now % 3600))


def time_until_time(seconds, seen=None, _time=time):
    current_seconds = seen or _time() % 3600
    if current_seconds > seconds:
        return seconds + 3600 - current_seconds
    elif current_seconds + 3600 < seconds:
        return seconds - 3600 - current_seconds
    else:
        return seconds - current_seconds


def get_address():
    if conf.MANAGER_ADDRESS:
        return conf.MANAGER_ADDRESS
    if platform == 'win32':
        return r'\\.\pipe\monocle'
    if hasattr(socket, 'AF_UNIX'):
        return join(conf.DIRECTORY, 'monocle.sock')
    return ('127.0.0.1', 5001)


def load_pickle(name, raise_exception=False):
    location = join(conf.DIRECTORY, 'pickles', '{}.pickle'.format(name))
    try:
        with open(location, 'rb') as f:
            return pickle_load(f)
    except (FileNotFoundError, EOFError):
        if raise_exception:
            raise FileNotFoundError
        else:
            return None


def dump_pickle(name, var):
    folder = join(conf.DIRECTORY, 'pickles')
    try:
        mkdir(folder)
    except FileExistsError:
        pass
    except Exception as e:
        raise OSError("Failed to create 'pickles' folder, please create it manually") from e

    location = join(folder, '{}.pickle'.format(name))
    with open(location, 'wb') as f:
        pickle_dump(var, f, HIGHEST_PROTOCOL)


def load_accounts():
    pickled_accounts = load_pickle('accounts')

    if conf.ACCOUNTS_CSV:
        accounts = load_accounts_csv()
        if pickled_accounts and set(pickled_accounts) == set(accounts):
            return pickled_accounts
        else:
            accounts = accounts_from_csv(accounts, pickled_accounts)
    elif conf.ACCOUNTS:
        if pickled_accounts and set(pickled_accounts) == set(acc[0] for acc in conf.ACCOUNTS):
            return pickled_accounts
        else:
            accounts = accounts_from_config(pickled_accounts)
    else:
        raise ValueError('Must provide accounts in a CSV or your config file.')

    dump_pickle('accounts', accounts)
    return accounts


def load_accounts_csv():
    csv_location = join(conf.DIRECTORY, conf.ACCOUNTS_CSV)
    with open(csv_location, 'rt') as f:
        accounts = {}
        reader = DictReader(f)
        for row in reader:
            accounts[row['username']] = dict(row)
    return accounts


def randomize_point(point, amount=0.0003, randomize=uniform):
    '''Randomize point, by up to ~47 meters by default.'''
    lat, lon = point
    return (
        randomize(lat - amount, lat + amount),
        randomize(lon - amount, lon + amount)
    )
