from datetime import datetime
from typing import *
import requests
import logging
from dateutil import parser
from dotenv import load_dotenv
import os
import requests

load_dotenv()



resource_urls = {
    "location": "https://api.resrobot.se/v2.1/location.name",
    "trip": "https://api.resrobot.se/v2.1/trip"
}

# Minimum number of trips we want to have cached
NUM_TRIPS = 5

class trafiklab():
    """A class for querying the Trafiklab API (trafiklab.se)
    """

    def init(self, api_key: str):
        """Initialize the class

        Args:
            api_key (str): Your own ResRobot 2.1 API key from Trafiklab.se
        """
        self.api_key = api_key

    def _api(self, resource: str, params: dict) -> dict:
        """Call a resource in the API, return dict of response.

        Args:
            resource (str): "location" or "trip".
            params (dict): parameters for the resource.

        Raises:
            Exception: in case of an invalid resource.

        Returns:
            dict: raw response from the API.
        """
        if not resource in resource_urls:
            raise Exception("Resource '%s' not found in API" % (resource))
        self.API_KEY = os.getenv("API_KEY")
        api_params = {
            "accessId": self.API_KEY,
            "format": "json",
        }
        api_params.update(params)
        try:
            r = requests.get(resource_urls[resource], params = api_params)
            logging.debug("Returned: " + str(r.text))
            return r.json()
        except Exception:
            logging.error("Trafiklab API caused exception", exc_info=True)
            return None


    def lookup(self, stop: str) -> Union[list, None]:
        """Lookup a named bus stop. Please not that the API is quite
        'forgiving' and does a partial match of the name. This means that
        you will get a response for most names, eg. 'sfdsffdfs' will return
        a large list. You need the 'id' for querying the trip(...) method.

        See https://www.trafiklab.se/api/resrobot-reseplanerare/platsuppslag
        for a description of the returned data.

        Args:
            stop (str): Name, or partial name, of bus stop.

        Returns:
            Union[list, None]: A list of dicts of matching(-ish) bus stops.
        """
        r = self._api("location", {"input": stop})
        if "stopLocationOrCoordLocation" in r:
            r = r["stopLocationOrCoordLocation"]
            return r
        else:
            return None

    def trip(self, from_id: int, to_id: int, context = None) -> Union[list, None]:
        """Lookup a trip using IDs from the lookup(...) method. Plese note that any
        possible trip will be returned so you might want to filter the results. If you
        search for a usual 20-minute bus trip from home to work the API will happily
        suggest a 45 minute alternative with bus changes.

        See https://www.trafiklab.se/api/resrobot-reseplanerare/sok-resa
        for a description of the returned data.

        Args:
            from_id (int): ID of origin stop.
            to_id (int): ID of destination stop.
            context ([type], optional): Context parameters for searching for additional trips
                                        This is the 'scrF' value of the previous call.

        Returns:
            Union[list, None]: A list of trips or None if none are found.
        """
        params = {"originId": from_id, "destId": to_id}
        if context is not None:
            params["context"] = context
        r = self._api("trip", params)
        if "Trip" in r:
            return r
        else:
            return None

class tripmonitor():
    """A class for monitoring trips from one location to another.
    The class caches API lookups keeping traffic to a minimum.
    """

    def init(self, linger_time: int, api_key: str):
        """Initialize the class

        Args:
            linger_time (int): The time in minutes you need to get to the bus.
                               Trips leaving within this time will be ignored.
            api_key (str): Your own Trafiklab.se API key.
        """
        self.linger_time = linger_time
        self.api = trafiklab()
        self.api.init(api_key)
        # Routes to query. A list of dicts: "from_id": "to_id"
        self.routes = []
        # Cached routes. A list of dicts: "from": "<from name>",
        #                                 "to":  "<to name>",
        #                                 "departure":  "datetime.datetime",
        #                                 "arrival":  "datetime.datetime",
        #                                 "line":  "<bus line>"
        self.route_cache = []
        # A list of bus lines we want omitted from the response
        self.blacklist = []
        # A dict of bus stops: "Name" : "<stop_id>"
        self.stop_cache = {}
        # Current loaded routes
        self.trips = []


    def add_route(self, origin: str, destination: str) -> bool:
        """Add route to monitor

        Args:
            origin (str): Name or origin, must match one single bus stop
            destination (str): Name or destination, must match one single bus stop

        Returns:
            bool: True if origin and destination matched exactly one bus stop, False otherwise
        """
        if not origin in self.stop_cache:
            stops = self.api.lookup(origin)
            if stops is None or len(stops) == 0:
                logging.error("Could not lookup origin '%s'" % (origin))
                return False
            else:
                logging.debug("%s : %s" % (origin, stops[0]["StopLocation"]["extId"]))
                self.stop_cache[origin] = stops[0]["StopLocation"]["extId"]
        if not destination in self.stop_cache:
            stops = self.api.lookup(destination)
            if stops is None or len(stops) == 0:
                logging.error("Could not lookup destination '%s'" % (destination))
                return False
            else:
                logging.debug("%s : %s" % (destination, stops[0]["StopLocation"]["extId"]))
                self.stop_cache[destination] = stops[0]["StopLocation"]["extId"]
        self.routes.append({"origin": origin, "destination": destination})
        return True


    def blacklist_line(self, line: str):
        """Blacklist a line. If you know a line occuring in the suggested routes that
           you want to avoid, add it to the black list

        Args:
            line (str): Line to be blacklisted
        """
        if not line in self.blacklist:
            self.blacklist.append(line)


    def dump(self):
        """Dump all trips
        """
        for trip in self.trips:
            logging.info(trip)


    def purge(self):
        """Remove all cached trips that have left or leavs within self.linger_time
        """
        removals = []
        for trip in self.trips:
            dt = trip["time"]
            now = datetime.now()
            diff = dt - now
            diff = diff.total_seconds() / 60
            if diff < self.linger_time:
                logging.debug("Purging %s at %s" % (trip["line"], dt))
                removals.append(trip)
        for trip in removals:
            self.trips.remove(trip)


    def refresh(self, context: str = None):
        """Refresh list of trips. New trips will be queryed if the number of
           known trips drop below NUM_TRIPS. You may therefore call refresh()
           continously without hammering the API.

        Args:
            context (str, optional): Used internally, please ignore.
        """
        self.purge()
        if len(self.trips) >= NUM_TRIPS:
            return
        for route in self.routes:
            o = self.stop_cache[route["origin"]]
            d = self.stop_cache[route["destination"]]
            j = self.api.trip(o, d, context)
            for t in j["Trip"]:
                origin = t["LegList"]["Leg"][0]["Origin"]
                destination = t["LegList"]["Leg"][0]["Destination"]
                line = t["LegList"]["Leg"][0]["Product"][0]["num"]
                dt = parser.parse("%s %s" % (origin["date"], origin["time"]))
                if line not in self.blacklist:
                    trip = {"line": line, "time": dt, "from": origin["name"], "to": destination["name"]}
                    if not trip in self.trips:
                        now = datetime.now()
                        diff = dt - now
                        diff = diff.total_seconds() / 60
                        if diff > self.linger_time:
                            logging.debug("%s to %s leaves at %s" % (line, destination["name"], dt))
                            self.trips.append(trip)
                        else:
                            logging.warning("Ignoring %s" % (dt))
        if context is None and len(self.trips) < NUM_TRIPS:
            self.refresh(j["scrF"])