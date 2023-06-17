#!/usr/bin/env python3
import argparse
import itertools
import json
import time
from datetime import datetime

import api
from db import DataBase


def main(user_id: str, session_token: str) -> None:
    db = DataBase()
    start_at = datetime.now()
    print('start_at', start_at)
    likes = 0
    pure_api = api.PureApi(user_id, session_token)
    for page in itertools.count(1):
        data = pure_api.get_next(start_at, page)
        if not data['results']:
            break
        for row in data['results']:
            was_liked = row['reactions']['outgoing_like']
            if not was_liked:
                if not db.was_liked(row['user_id']):
                    pure_api.set_like(row['user_id'])
                    db.set_like(row['user_id'], json.dumps(row, ensure_ascii=False))
                    likes += 1
                    time.sleep(1)
                    continue
            db.update_like(row['user_id'], json.dumps(row, ensure_ascii=False))
        print(f'{page=}, {likes=}', end='\r')
    print()

    end_at = start_at
    while True:
        start_at = datetime.now()
        data = pure_api.get_new(start_at, end_at)
        end_at = start_at
        for row in data['results']:
            was_liked = row['reactions']['outgoing_like']
            if not was_liked:
                if not db.was_liked(row['user_id']):
                    pure_api.set_like(row['user_id'])
                    db.set_like(row['user_id'], row)
                    likes += 1
                    time.sleep(1)
                    continue
            db.update_like(row['user_id'], json.dumps(row, ensure_ascii=False))
        now_time = datetime.now().strftime('%H:%M:%S')
        print(f'time={now_time}, {likes=}', end='\r')
        time.sleep(60)


def stats() -> None:
    db = DataBase()
    print('count:', db.get_like_count())


def search(query: str) -> None:
    db = DataBase()
    for created_at, data in db.search(query):
        print(created_at, repr(json.loads(data)['announcement_text']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action', required=True)
    parser_like = subparsers.add_parser('like')
    parser_like.add_argument('user_id')
    parser_like.add_argument('token')
    subparsers.add_parser('stats')
    parser_search = subparsers.add_parser('search')
    parser_search.add_argument('query')
    args = parser.parse_args()
    if args.action == 'like':
        main(args.user_id, args.token)
    elif args.action == 'stats':
        stats()
    elif args.action == 'search':
        search(args.query)
