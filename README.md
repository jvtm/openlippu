# openlippu

Script (and Python API) for accessing [rastilippu.fi](https://www.rastilippu.fi),
the new [official](https://www.suunnistus.fi) info site for
open course / motion orienteering events in Finland.

For now just a script for dumping event list to JSON.

## `liput.py`

Python 3.x script for dumping daily/weekly/monthly event lists to JSON.

Example run:

```bash
$ ./liput.py --period week --limit 2
writing 16 items to rastilippu-week-20180326-20180401-pretty.json
writing 18 items to rastilippu-week-20180402-20180408-pretty.json
```

The script does not use any of the coordinate base filtering. It looks like that the API gives maximum 50 events at a time,
and there are no hints about possible pagination. Weekly lists seem to be OK for now.


JSON info for a single event:

```json
    $ cat rastilippu-week-20180326-20180401-pretty.json | jq '.[] | select(.event.locationAddress | contains("Esbo"))'
    {
      "event": {
        "currentAttendeeCount": 8,
        "endDateTime": 1522582200000,
        "eventId": 6717,
        "locationAddress": "Klovisåkersvägen 1, 02180 Esbo, Finland",
        "locationCoordinates": {
          "lat": 60.20369,
          "lon": 24.756649
        },
        "locationDescription": "Hills Business Park, Klovinpellontie 1-3, Espoo",
        "maxAttendeeCount": 10000,
        "name": "Mankkaa",
        "organizerId": 7020,
        "organizerName": "Espoon Akilles ry",
        "parentSeriesEventId": 6718,
        "parentSeriesEventName": "Korttelirastit",
        "parentSeriesEventUuid": "a153c1e2-0b45-493d-8f28-c722020c3bf8",
        "priceInCents": 500,
        "sports": [],
        "startDateTime": 1522576800000,
        "uuid": "160529f4-d89b-4667-a733-478c9ec234cd"
      },
      "serviceAvailable": true
    }
```


## Why?

The official page has some flaws:

* Finnish only
* map based search is cumbersome to use, and might limit
* also the event list mode reacts to map coordinates -> not getting the true, full list!
* there doesn't seem to be any kind of full text search
* browsing thru the results might not be the easiest interface either, and at this point it is unknown whether event organizers will provide also their own (simpler) traditional result pages
* most likely not indexed by any seatch engines (no robots.txt tho...)


Now, the good thing is that the service _does_ have JSON API. _So lets use it!_

Also worth noting that the previous [kunto.suunnistus.fi](http://kunto.suunnistus.fi/) seems to be abandoned.


## JSON API

_Some of the reverse engineered details to appear here..._

* public
* event list, uuids
* searches and listing (dates, coordinates, ...)
* auth: some info is (supposedly) behind authentication (one time password over sms -> session cookies)


## Ideas, TODOs, ...

* collect (regularly updated) JSON listings via static pages somewhere for easier consumption
* archive result lists (altho lets check usage terms etc first...)
* dump simple HTML output...
* ...and setup a cron job for JSON dumps, HTML listing on a public server
* investigate all other API end points, including authenticated ones
* getting the proper authnz token(s), cookie store etc should be relatively simple...

