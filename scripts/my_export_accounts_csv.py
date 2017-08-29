#!/usr/bin/env python3

import csv
import sys

from datetime import datetime
from pathlib import Path

monocle_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(monocle_dir))

from monocle.shared import ACCOUNTS

accounts_file = monocle_dir / 'accounts.csv'
try:
    now = datetime.now().strftime("%Y-%m-%d-%H%M")
    accounts_file.rename('accounts-{}.csv'.format(now))
except FileNotFoundError:
    pass

banned = []
invalid = []
underlevel = []

with accounts_file.open('w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(('username', 'password', 'provider', 'model', 'iOS', 'id'))
    for account in ACCOUNTS.values():
        if account.get('banned', False):
            banned.append(account)
            continue
        if not account.get('level', False):
            invalid.append(account)
            continue
        if account.get('level') < 2:
            underlevel.append(account)
        writer.writerow((account['username'],
                         account['password'],
                         account['provider'],
                         account['model'],
                         account['iOS'],
                         account['id']))

if banned:
    banned_file = monocle_dir / 'banned.csv'
    write_header = not banned_file.exists()
    with banned_file.open('a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(('username', 'password', 'provider', 'level', 'created', 'last used'))
        for account in banned:
            row = [account['username'], account['password'], account['provider']]
            row.append(account.get('level'))
            try:
                row.append(datetime.fromtimestamp(account['created']).strftime('%x %X'))
            except KeyError:
                row.append(None)
            try:
                row.append(datetime.fromtimestamp(account['time']).strftime('%x %X'))
            except KeyError:
                row.append(None)
            writer.writerow(row)

if invalid:
    invalid_file = monocle_dir / 'invalid.csv'
    write_header = not invalid_file.exists()
    with invalid_file.open('a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(('username', 'password', 'provider', 'model', 'iOS', 'id'))
        for account in invalid:
            row = [account['username'], account['password'], account['provider']]
            writer.writerow(row)

if underlevel:
    underlevel_file = monocle_dir / 'underlevel.csv'
    write_header = not underlevel_file.exists()
    with underlevel_file.open('a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(('username', 'password', 'provider', 'model', 'iOS', 'id'))
        for account in underlevel:
            row = [account['username'], account['password'], account['provider'], account['model'], account['iOS'], account['id']]
            writer.writerow(row)

print('Done!')
