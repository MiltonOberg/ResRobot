from dotenv import load_dotenv
import os
import requests
import trafiklab
import sys
import logging

load_dotenv()

API_KEY = os.getenv("API_KEY")

try:
    import coloredlogs
except ModuleNotFoundError:
    print("Sorry, but I am rather fond of coloredlogs")
    print("sudo -H python -m pip install coloredlogs")
    sys.exit(1)

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG" if "-d" in sys.argv else "INFO", fmt='%(asctime)s,%(msecs)03d %(name)s %(levelname)-8s %(filename)s:%(lineno)d %(message)s')

t = trafiklab.tripmonitor()
# No use in presenting buses we cannot catch unless we run for our lives
time_to_walk_to_the_bus_stop_in_minutes = 15
t.init(time_to_walk_to_the_bus_stop_in_minutes, API_KEY)
# Partial names are supported. The full names below are
# "Dalby busstation (Lund kn)" and "Lund Centralstation"
if not t.add_route("Dalby Buss", "Lund Central"):
    logging.error("Failed to add route")
    sys.exit(1)
# The API returns "possible" routes which can be very far from "desirable" routes
t.blacklist_line("174")
logging.info("Refreshing")
t.refresh()
t.dump()
logging.info("Refreshing")
t.refresh()
t.dump()