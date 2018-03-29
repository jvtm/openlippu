#!/usr/bin/env python3
"""
Script for accessing rastilippu.fi event info

Might later on get modified to be a proper API library,
but this is good enough for now.

WORK IN PROGRESS: API / Library version might appear soon,
and also some tooling to make a super simplified HTML listing.


https://www.rastilippu.fi/api/events/search/?
    dateTimeRangeStart=2018-03-11T00:00:00%2B02:00
    dateTimeRangeEnd=2018-12-01T00:00:00%2B03:00

    -> list of event info objs
 + also corners for range select
 + pagination? api seems to give max 50 entries at a time; reducing the time period helps

For now, just dumps to disk.

class + more API operations to follow at some point

Link to event:
 https://www.rastilippu.fi/kuntorastit/tapahtuma/<uuid>

Result list:
 /api/result/event/
     -> list of short event info objs (not as much info as search api)

Courses in single event:
curl 'https://www.rastilippu.fi/api/results/event/ff7ce9c3-a624-4ca6-8bbd-fb87f9d42813/courses'

https://www.rastilippu.fi/api/results/event/ff7ce9c3-a624-4ca6-8bbd-fb87f9d42813

+ some kind of search too -> gets detailed event info
 -> there seem to be duplicate results / no caching?
 -> search seems generic, and therefore... vulnerable?

Copyright (c) 2018 Jyrki Muukkonen
Licensed under the MIT license. See LICENSE.txt for details.
"""
import argparse
import json
import os
import sys

import arrow
import requests


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://www.rastilippu.fi")
    parser.add_argument("--date-from", type=arrow.get)
    parser.add_argument("--date-to", type=arrow.get)
    parser.add_argument("--period", default="week", choices=["day", "week", "month"])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--raw", default=False, action="store_true", help="Dump original contents (default is prettified JSON)")
    parser.add_argument("--overwrite", default=False, action="store_true", help="Overwrite existing files")
    args = parser.parse_args(argv)

    if args.date_from is None:
        args.date_from = arrow.now()

    # must have either limit or end date
    # if missing both, get nice enough limit based on single request period
    if args.limit is None and args.date_to is None:
        if args.period == "day":
            args.limit = 14
        elif args.period == "week":
            args.limit = 4
        elif args.period == "month":
            args.limit = 3

    session = requests.Session()
    url = args.base_url + "/api/events/search/"

    for d_from, d_to in arrow.Arrow.span_range(args.period, args.date_from, args.date_to, limit=args.limit):
        params = {
            "dateTimeRangeStart": d_from.isoformat(),
            "dateTimeRangeEnd": d_to.isoformat(),
        }
        resp = session.get(url, params=params)
        resp.raise_for_status()     # Note: errors are json too, but we not really caring yet. Just crash.
        fname = "rastilippu-{period}-{dfrom}-{dto}-{fmt}.json".format(
            period=args.period,
            dfrom=d_from.strftime("%Y%m%d"),
            dto=d_to.strftime("%Y%m%d"),
            fmt="raw" if args.raw else "pretty",
        )
        if os.path.exists(fname):
            if args.overwrite:
                print("overwriting {}".format(fname))
            else:
                print("{} already exists".format(fname))
                continue

        if args.raw:
            print("writing {} bytes to {}".format(len(resp.content), fname))
            with open(fname, "wb") as out:
                out.write(resp.content)
        else:
            # validates, re-indents, sorts keys
            info = resp.json()
            print("writing {} items to {}".format(len(info), fname))
            if len(info) == 50:
                print("NOTE: there might be more events available (got exactly 50)")
            with open(fname, "w") as out:
                json.dump(resp.json(), out, sort_keys=True, indent=4)
                out.write("\n")


if __name__ == '__main__':
    sys.exit(main())
