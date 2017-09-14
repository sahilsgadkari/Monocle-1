### All lines that are commented out (and some that aren't) are optional ###

DB_ENGINE = 'sqlite:///db.sqlite'
#DB_ENGINE = 'mysql://user:pass@localhost/monocle'
#DB_ENGINE = 'postgresql://user:pass@localhost/monocle

AREA_NAME = 'SLC'     # the city or region you are scanning
LANGUAGE = 'EN'       # ISO 639-1 codes EN, DE, ES, FR, IT, JA, KO, PT, or ZH for Pokémon/move names
MAX_CAPTCHAS = 100    # stop launching new visits if this many CAPTCHAs are pending
SCAN_DELAY = 10       # wait at least this many seconds before scanning with the same account
SPEED_UNIT = 'miles'  # valid options are 'miles', 'kilometers', 'meters'
SPEED_LIMIT = 19.5    # limit worker speed to this many SPEED_UNITs per hour

# The number of simultaneous workers will be these two numbers multiplied.
# On the initial run, workers will arrange themselves in a grid across the
# rectangle you defined with MAP_START and MAP_END.
# The rows/columns will also be used for the dot grid in the console output.
# Provide more accounts than the product of your grid to allow swapping.
GRID = (4, 4)  # rows, columns

# the corner points of a rectangle for your workers to spread out over before
# any spawn points have been discovered
MAP_START = (40.7913, -111.9398)
MAP_END = (40.7143, -111.8046)

# do not visit spawn points outside of your MAP_START and MAP_END rectangle
# the boundaries will be the rectangle created by MAP_START and MAP_END, unless
STAY_WITHIN_MAP = True

# ensure that you visit within this many meters of every part of your map during bootstrap
# lower values are more thorough but will take longer
BOOTSTRAP_RADIUS = 120

GIVE_UP_KNOWN = 75   # try to find a worker for a known spawn for this many seconds before giving up
GIVE_UP_UNKNOWN = 60 # try to find a worker for an unknown point for this many seconds before giving up
SKIP_SPAWN = 90      # don't even try to find a worker for a spawn if the spawn time was more than this many seconds ago

# How often should the mystery queue be reloaded (default 90s)
# this will reduce the grouping of workers around the last few mysteries
#RESCAN_UNKNOWN = 90

# filename of accounts CSV
ACCOUNTS_CSV = 'accounts.csv'

# the directory that the pickles folder, socket, CSV, etc. will go in
# defaults to working directory if not set
#DIRECTORY = None

# Limit the number of simultaneous logins to this many at a time.
# Lower numbers will increase the amount of time it takes for all workers to
# get started but are recommended to avoid suddenly flooding the servers with
# accounts and arousing suspicion.
SIMULTANEOUS_LOGINS = 4

# Limit the number of workers simulating the app startup process simultaneously.
SIMULTANEOUS_SIMULATION = 10

# Immediately select workers whose speed are below (SPEED_UNIT)p/h instead of
# continuing to try to find the worker with the lowest speed.
# May increase clustering if you have a high density of workers.
GOOD_ENOUGH = 0.1

# Seconds to sleep after failing to find an eligible worker before trying again.
SEARCH_SLEEP = 2.5

## alternatively define a Polygon to use as boundaries (requires shapely)
## if BOUNDARIES is set, STAY_WITHIN_MAP will be ignored
## more information available in the shapely manual:
## http://toblerity.org/shapely/manual.html#polygons
#from shapely.geometry import Polygon
#BOUNDARIES = Polygon(((40.799609, -111.948556), (40.792749, -111.887341), (40.779264, -111.838078), (40.761410, -111.817908), (40.728636, -111.805293), (40.688833, -111.785564), (40.689768, -111.919389), (40.750461, -111.949938)))

# key for Bossland's hashing server, otherwise the old hashing lib will be used
#HASH_KEY = '9d87af14461b93cb3605'  # this key is fake

# Skip PokéStop spinning and egg incubation if your request rate is too high
# for your hashing subscription.
# e.g.
#   75/150 hashes available 35/60 seconds passed => fine
#   70/150 hashes available 30/60 seconds passed => throttle (only scan)
# value: how many requests to keep as spare (0.1 = 10%), False to disable
#SMART_THROTTLE = 0.1

# Swap the worker that has seen the fewest Pokémon every x seconds
# Defaults to whatever will allow every worker to be swapped within 6 hours
#SWAP_OLDEST = 300  # 5 minutes
# Only swap if it's been active for more than x minutes
#MINIMUM_RUNTIME = 10

### these next 6 options use more requests but look more like the real client
APP_SIMULATION = True     # mimic the actual app's login requests
COMPLETE_TUTORIAL = True  # complete the tutorial process and configure avatar for all accounts that haven't yet
INCUBATE_EGGS = True        # incubate eggs if available

## encounter Pokémon to store IVs.
## valid options:
# 'all' will encounter every Pokémon that hasn't been already been encountered
# 'notifying' will encounter Pokémon that are eligible for notifications
# None will never encounter Pokémon
#ENCOUNTER = 'notifying'
ENCOUNTER = 'some'
ENCOUNTER_IDS = { 201 }

# PokéStops
SPIN_POKESTOPS = True # spin all PokéStops that are within range
SPIN_COOLDOWN = 300    # spin only one PokéStop every n seconds (default 300)

# minimum number of each item to keep if the bag is cleaned
# remove or set to None to disable bag cleaning
# automatically disabled if SPIN_POKESTOPS is disabled
# triple quotes are comments, remove them to use this ITEM_LIMITS example
ITEM_LIMITS = {
    1:    20,  # Poké Ball
    2:    40,  # Great Ball
    3:    50,  # Ultra Ball
    101:   0,  # Potion
    102:   0,  # Super Potion
    103:   0,  # Hyper Potion
    104:  20,  # Max Potion
    201:   0,  # Revive
    202:  20,  # Max Revive
    701:  10,  # Razz Berry
    702:  20,  # Bluk Berry
    703:  10,  # Nanab Berry
    704:  20,  # Wepar Berry
    705:  10,  # Pinap Berry
}


# Update the console output every x seconds
REFRESH_RATE = 0.75  # 750ms
# Update the seen/speed/visit/speed stats every x seconds
STAT_REFRESH = 5

# sent with GET_PLAYER requests, should match your region
PLAYER_LOCALE = {'country': 'US', 'language': 'en', 'timezone': 'America/Los Angeles'}

# retry a request after failure this many times before giving up
MAX_RETRIES = 3

# number of seconds before timing out on a login request
LOGIN_TIMEOUT = 2.5

# add spawn points reported in cell_ids to the unknown spawns list
#MORE_POINTS = False

# Set to True to kill the scanner when a newer version is forced
#FORCED_KILL = False

# exclude these Pokémon from the map by default (only visible in trash layer)
TRASH_IDS = (
    16, 19, 21, 29, 32, 41, 46, 48, 50, 52, 56, 74, 77, 96, 111, 133,
    161, 163, 167, 177, 183, 191, 194
)

# include these Pokémon on the "rare" report
RARE_IDS = (3, 6, 9, 45, 62, 71, 80, 85, 87, 89, 91, 94, 114, 130, 131, 134)

from datetime import datetime
REPORT_SINCE = datetime(2017, 2, 17)  # base reports on data from after this date

# used for altitude queries and maps in reports
#GOOGLE_MAPS_KEY = 'OYOgW1wryrp2RKJ81u7BLvHfYUA6aArIyuQCXu4'  # this key is fake
REPORT_MAPS = True  # Show maps on reports
#ALT_RANGE = (1250, 1450)  # Fall back to altitudes in this range if Google query fails

## Round altitude coordinates to this many decimal places
## More precision will lead to larger caches and more Google API calls
## Maximum distance from coords to rounded coords for precisions (at Lat40):
## 1: 7KM, 2: 700M, 3: 70M, 4: 7M
#ALT_PRECISION = 2

## Automatically resolve captchas using 2Captcha key.
#CAPTCHA_KEY = '1abc234de56fab7c89012d34e56fa7b8'
## the number of CAPTCHAs an account is allowed to receive before being swapped out
#CAPTCHAS_ALLOWED = 3
## Get new accounts from the CAPTCHA queue first if it's not empty
#FAVOR_CAPTCHA = True

# allow displaying the live location of workers on the map
MAP_WORKERS = True
# filter these Pokemon from the map to reduce traffic and browser load
#MAP_FILTER_IDS = [161, 165, 16, 19, 167]

# unix timestamp of last spawn point migration, spawn times learned before this will be ignored
LAST_MIGRATION = 1496448000 # June 3, 2017

# Treat a spawn point's expiration time as unknown if nothing is seen at it on more than x consecutive visits
FAILURES_ALLOWED = 3

## Map data provider and appearance, previews available at:
## https://leaflet-extras.github.io/leaflet-providers/preview/
#MAP_PROVIDER_URL = '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
#MAP_PROVIDER_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

# set of proxy addresses and ports
# SOCKS requires aiosocks to be installed
#PROXIES = {'http://127.0.0.1:8080', 'https://127.0.0.1:8443', 'socks5://127.0.0.1:1080'}

# convert spawn_id to integer for more efficient DB storage, set to False if
# using an old database since the data types are incompatible.
#SPAWN_ID_INT = True

# Bytestring key to authenticate with manager for inter-process communication
#AUTHKEY = b'm3wtw0'
# Address to use for manager, leave unset or set to None if you're note sure.
#MANAGER_ADDRESS = r'\\.\pipe\monocle'  # must be in this format for Windows
#MANAGER_ADDRESS = 'monocle.sock'       # the socket name for Unix systems
#MANAGER_ADDRESS = ('127.0.0.1', 5002)    # could be used for CAPTCHA solving and live worker maps on remote systems

# Store the cell IDs so that they don't have to be recalculated every visit.
# Highly recommended unless you don't have enough memory for them.
# Disabling will increase processor usage.
#CACHE_CELLS = True

# Only for use with web-sanic (requires PostgreSQL)
#DB = {'host': '127.0.0.1', 'user': 'monocle_role', 'password': 'pik4chu', 'port': '5432', 'database': 'monocle'}

# Disable to use Python's event loop even if uvloop is installed
#UVLOOP = True

# The number of coroutines that are allowed to run simultaneously.
#COROUTINES_LIMIT = GRID[0] * GRID[1]

### FRONTEND CONFIGURATION
LOAD_CUSTOM_HTML_FILE = False # File path MUST be 'templates/custom.html'
LOAD_CUSTOM_CSS_FILE = False  # File path MUST be 'static/css/custom.css'
LOAD_CUSTOM_JS_FILE = False  # File path MUST be 'static/js/custom.js'

#FB_PAGE_ID = None
#TWITTER_SCREEN_NAME = None  # Username withouth '@' char
#DISCORD_INVITE_ID = None
#TELEGRAM_USERNAME = None  # Username withouth '@' char

## Variables below will be used as default values on frontend
FIXED_OPACITY = False  # Make marker opacity independent of remaining time
SHOW_TIMER = False  # Show remaining time on a label under each pokemon marker

### OPTIONS BELOW THIS POINT ARE ONLY NECESSARY FOR NOTIFICATIONS ###
NOTIFY = True  # enable notifications

# create images with Pokémon image and optionally include IVs and moves
# requires cairo and ENCOUNTER = 'notifying' or 'all'
TWEET_IMAGES = True
# IVs and moves are now dependant on level, so this is probably not useful
IMAGE_STATS = False

# As many hashtags as can fit will be included in your tweets, these will
# be combined with landmark-specific hashtags (if applicable).
HASHTAGS = {AREA_NAME, 'Monocle', 'PokemonGO'}
#TZ_OFFSET = 0  # UTC offset in hours (if different from system time)

# the required number of seconds remaining to notify about a Pokémon
TIME_REQUIRED = 600  # 10 minutes

### Only set either the NOTIFY_RANKING or NOTIFY_IDS, not both!
# The (x) rarest Pokémon will be eligible for notification. Whether a
# notification is sent or not depends on its score, as explained below.
NOTIFY_RANKING = None

# Pokémon to potentially notify about, in order of preference.
# The first in the list will have a rarity score of 1, the last will be 0.
NOTIFY_IDS = None

# Sightings of the top (x) will always be notified about, even if below TIME_REQUIRED
# (ignored if using NOTIFY_IDS instead of NOTIFY_RANKING)
ALWAYS_NOTIFY = 14

# Always notify about the following Pokémon even if their time remaining or scores are not high enough
ALWAYS_NOTIFY_IDS = {3,6,9,26,40,45,62,65,68,71,80,83,87,94,103,108,110,113,115,117,122,130,131,132,137,142,143,144,145,146,147,148,149,150,151,154,157,159,160,172,173,174,175,176,181,182,186,189,192,195,196,197,199,201,205,208,212,214,221,222,225,230,232,233,235,236,237,238,239,240,242,243,244,245,246,247,248,249,250,251}

# Never notify about the following Pokémon, even if they would otherwise be eligible
#NEVER_NOTIFY_IDS = { }

# Override the rarity score for particular Pokémon
# format is: {pokemon_id: rarity_score}
#RARITY_OVERRIDE = {148: 0.6, 149: 0.9}

# Ignore IV score and only base decision on rarity score (default if IVs not known)
IGNORE_IVS = True

# Ignore rarity score and only base decision on IV score
#IGNORE_RARITY = False

# The Pokémon score required to notify goes on a sliding scale from INITIAL_SCORE
# to MINIMUM_SCORE over the course of FULL_TIME seconds following a notification
# Pokémon scores are an average of the Pokémon's rarity score and IV score (from 0 to 1)
# If NOTIFY_RANKING is 90, the 90th most common Pokémon will have a rarity of score 0, the rarest will be 1.
# IV score is the IV sum divided by 45 (perfect IVs).
FULL_TIME = 1800  # the number of seconds after a notification when only MINIMUM_SCORE will be required
INITIAL_SCORE = 0.7  # the required score immediately after a notification
MINIMUM_SCORE = 0.4  # the required score after FULL_TIME seconds have passed


### The following values are fake, replace them with your own keys to enable
### notifications, otherwise leave them out of your config or set them to None.
### You must provide keys for at least one service to use notifications.

#PB_API_KEY = 'o.9187cb7d5b857c97bfcaa8d63eaa8494'
#PB_CHANNEL = 0  # set to the integer of your channel, or to None to push privately

#TWITTER_CONSUMER_KEY = '53d997264eb7f6452b7bf101d'
#TWITTER_CONSUMER_SECRET = '64b9ebf618829a51f8c0535b56cebc808eb3e80d3d18bf9e00'
#TWITTER_ACCESS_KEY = '1dfb143d4f29-6b007a5917df2b23d0f6db951c4227cdf768b'
#TWITTER_ACCESS_SECRET = 'e743ed1353b6e9a45589f061f7d08374db32229ec4a61'

## Telegram bot token is the one Botfather sends to you after completing bot creation.
## Chat ID can be two different values:
## 1) '@channel_name' for channels
## 2) Your chat_id if you will use your own account. To retrieve your ID, write to your bot and check this URL:
##     https://api.telegram.org/bot<BOT_TOKEN_HERE>/getUpdates
#TELEGRAM_BOT_TOKEN = '123456789:AA12345qT6QDd12345RekXSQeoZBXVt-AAA'
#TELEGRAM_CHAT_ID = '@your_channel'

#WEBHOOKS = {'http://127.0.0.1:4000'}


##### Referencing landmarks in your tweets/notifications

#### It is recommended to store the LANDMARKS object in a pickle to reduce startup
#### time if you are using queries. An example script for this is in:
#### scripts/pickle_landmarks.example.py
#from pickle import load
#with open('pickles/landmarks.pickle', 'rb') as f:
#    LANDMARKS = load(f)

### if you do pickle it, just load the pickle and omit everything below this point

#from monocle.landmarks import Landmarks
#LANDMARKS = Landmarks(query_suffix=AREA_NAME)

# Landmarks to reference when Pokémon are nearby
# If no points are specified then it will query OpenStreetMap for the coordinates
# If 1 point is provided then it will use those coordinates but not create a shape
# If 2 points are provided it will create a rectangle with its corners at those points
# If 3 or more points are provided it will create a polygon with vertices at each point
# You can specify the string to search for on OpenStreetMap with the query parameter
# If no query or points is provided it will query with the name of the landmark (and query_suffix)
# Optionally provide a set of hashtags to be used for tweets about this landmark
# Use is_area for neighborhoods, regions, etc.
# When selecting a landmark, non-areas will be chosen first if any are close enough
# the default phrase is 'in' for areas and 'at' for non-areas, but can be overriden for either.

### replace these with well-known places in your area

## since no points or query is provided, the names provided will be queried and suffixed with AREA_NAME
#LANDMARKS.add('Rice Eccles Stadium', shortname='Rice Eccles', hashtags={'Utes'})
#LANDMARKS.add('the Salt Lake Temple', shortname='the temple', hashtags={'TempleSquare'})

## provide two corner points to create a square for this area
#LANDMARKS.add('City Creek Center', points=((40.769210, -111.893901), (40.767231, -111.888275)), hashtags={'CityCreek'})

## provide a query that is different from the landmark name so that OpenStreetMap finds the correct one
#LANDMARKS.add('the State Capitol', shortname='the Capitol', query='Utah State Capitol Building')

### area examples ###
## query using name, override the default area phrase so that it says 'at (name)' instead of 'in'
#LANDMARKS.add('the University of Utah', shortname='the U of U', hashtags={'Utes'}, phrase='at', is_area=True)
## provide corner points to create a polygon of the area since OpenStreetMap does not have a shape for it
#LANDMARKS.add('Yalecrest', points=((40.750263, -111.836502), (40.750377, -111.851108), (40.751515, -111.853833), (40.741212, -111.853909), (40.741188, -111.836519)), is_area=True)

################## CUSTOMIZED CONFIGURATION ITEMS FOR POGOSD ####################

## Show details like IV and Moves in Map
MAP_SHOW_DETAILS = False
SHOW_IV = False # Show IV below each pokemon marker

## For DARK_MAP_OPACITY and LIGHT_MAP_OPACITY choose value between 1.0 and 0.0
DARK_MAP_OPACITY = 0.80
DARK_MAP_PROVIDER_URL = 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png'
DARK_MAP_PROVIDER_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
LIGHT_MAP_OPACITY = 1.0
LIGHT_MAP_PROVIDER_URL = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
LIGHT_MAP_PROVIDER_ATTRIBUTION = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'

## Send Gym info to webhook(s). If True this will flood webhooks with Gym data since duplication of gym data still occurs
GYM_WEBHOOK = False

## Slow down how often Gym name is retrieved, not currently used though
#GYM_COOLDOWN

## Pull Gym name to populate Gym Table. This will populate a gym name cache upon initial startup. When set to true, consider clearing the fort DB from time to time as well as cache files. To clear fort DB, do so in this order: TRUNCATE fort_raids; TRUNCATE fort_sightings; TRUNCATE forts;. Then delete fort_names.pickle, forts.pickle, raids.pickle
PULL_GYM_NAME = True

## Show raid timers by default above raid icons
SHOW_RAID_TIMER = False

## Raid IDs to hide (filter) by default
RAID_IDS = (1,2)

## Show Unown letter (form) menu item to hide/display letter
SHOW_FORM_MENU_ITEM = False

## Default setting to hide/display Unown letter above Unown icon
SHOW_FORM = True

## If set to True, enables a splash message to be displayed once until the button is clicked to clear it. User will not see splash message again unless FORCE_SPLASH = True below.
SHOW_SPLASH = False

## Force splash message to show regardless of clicking clear button
FORCE_SPLASH = False

## If SHOW_SPLASH = True, the following configuration item changes the splash message from default which is currently a donation request plus a paypal button.  PAYPAL_BUTTON_CODE needs to be defined below for button to work correctly.
## Example: SPLASH_MESSAGE = 'Scans are currently only reporting Raids and Gyms due to shadow bans. We will work to restore full scanning capabilities ASAP.'
## Default: SPLASH_MESSAGE = 'Funding levels to maintain scans and maps are running low.<br>Please consider donating.<br><br>Thank you for your support.'
SPLASH_MESSAGE = None

## Show PayPal link if URL is provided below within ''. If set to None, the Donations tab will not be displayed on map settings. If PAYPAL_URL is defined, PAYPAL_BUTTON_CODE must be either defined or set to ''
PAYPAL_URL = None
PAYPAL_BUTTON_CODE = None

## Show monetary balances in Donations tab. For BALANCE and FUNDING_GOAL use single quotes ''
BALANCE = '352'
FUNDING_GOAL = '310'

## Default layers control. Anything set to True will have the layer shown on the map by default (checked)
SHOW_POKEMON_BY_DEFAULT = True
SHOW_GYMS_BY_DEFAULT = False
SHOW_RAIDS_BY_DEFAULT = False
SHOW_SCAN_AREA_BY_DEFAULT = True
SHOW_SPAWNPOINTS_BY_DEFAULT = False ## This shows both spawnpoints and workers

## Switch scan to Gym Scan Only Mode. This requires a modification to your database copying your gym points into a separate table and treating them as spawnpoints for workers to visit. Utilizes a minimal amount of workers to perform gym and raid scans.
## For mysql, utilize this query: CREATE TABLE gympoints SELECT * FROM spawnpoints; TRUNCATE gympoints; ALTER TABLE gympoints ADD PRIMARY KEY (id); ALTER TABLE gympoints MODIFY COLUMN id int(11) NOT NULL AUTO_INCREMENT; INSERT INTO gympoints (spawn_id, lat, lon) SELECT id, lat, lon FROM forts; UPDATE gympoints SET despawn_time = FLOOR(1 + RAND() * (3600 - 1)); UPDATE gympoints SET spawn_id = FLOOR(8854000000000 + RAND() * (8855000000000 - 8854000000000));
GYM_POINTS = False;

## For POGOSD_REGION blank should be '', region should be '/se_sd', '/sw_sd', etc. Used with nginx to statically change data URL data flows
POGOSD_REGION = ''

## If defined, displays a scrolling ticker across the top of the map frontend.
## Example: TICKER_ITEMS = '<p>Scans out of commission until further notice.</p><p>Shadow bans are resulting in complete bans.</p><p>You will not see Raids or Pokemon.</p>'
TICKER_ITEMS = None
TICKER_COLOR = 'yellow'  # Color choices are: red (default), orange, yellow

## If defined within '', displays a static splash screen on the map frontend.
## Example: MOTD = 'We are currently offline until further notice.'
MOTD = None

## For ANNOUNCEMENTS use the following for each line <li>blah blah</li><br><br>
#ANNOUNCEMENTS = None

