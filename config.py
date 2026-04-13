# ============================================================
# config.py
# ============================================================

# ── Google Places API ────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ── Google Sheets Config ─────────────────────────────────────
GOOGLE_SHEETS_CREDENTIALS_FILE = "credentials.json"
GOOGLE_SHEET_NAME              = "PetCare USA Animal Shelters"
GOOGLE_WORKSHEET_NAME          = "Sheet1"

# ── Search Settings ──────────────────────────────────────────
SEARCH_QUERY = "animal shelter"

# ── All 50 US States with major cities ──────────────────────
USA_CITIES = {  
    
    "Minnesota": [
        "Coon Rapids", "Burnsville", "Blaine", "Lakeville"
    ],
    "Mississippi": [
        "Jackson", "Gulfport", "Southaven", "Hattiesburg", "Biloxi",
        "Meridian", "Tupelo", "Olive Branch", "Greenville", "Horn Lake"
    ],
    "Missouri": [
        "Kansas City", "Saint Louis", "Springfield", "Columbia", "Independence",
        "Lee's Summit", "O'Fallon", "St. Joseph", "St. Charles", "Blue Springs",
        "Joplin", "Chesterfield", "Jefferson City", "Cape Girardeau", "Florissant"
    ],
    "Montana": [
        "Billings", "Missoula", "Great Falls", "Bozeman", "Butte",
        "Helena", "Kalispell", "Havre", "Anaconda"
    ],
    "Nebraska": [
        "Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney",
        "Fremont", "Hastings", "Norfolk", "Columbus", "North Platte"
    ],
    "Nevada": [
        "Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks",
        "Carson City", "Elko", "Mesquite", "Boulder City"
    ],
    "New Hampshire": [
        "Manchester", "Nashua", "Concord", "Derry", "Dover",
        "Rochester", "Salem", "Merrimack", "Hudson", "Portsmouth"
    ],
    "New Jersey": [
        "Newark", "Jersey City", "Paterson", "Elizabeth", "Edison",
        "Woodbridge", "Lakewood", "Toms River", "Hamilton", "Trenton",
        "Clifton", "Camden", "Brick", "Cherry Hill", "Passaic"
    ],
    "New Mexico": [
        "Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell",
        "Farmington", "Clovis", "Hobbs", "Alamogordo", "Carlsbad"
    ],
    "New York": [
        "New York City", "Buffalo", "Yonkers", "Rochester", "Syracuse",
        "Albany", "New Rochelle", "Mount Vernon", "Schenectady", "Utica",
        "White Plains", "Hempstead", "Troy", "Niagara Falls", "Binghamton"
    ],
    "North Carolina": [
        "Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem",
        "Fayetteville", "Cary", "Wilmington", "High Point", "Concord",
        "Asheville", "Gastonia", "Jacksonville", "Chapel Hill", "Rocky Mount"
    ],
    "North Dakota": [
        "Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo",
        "Williston", "Dickinson", "Mandan"
    ],
    "Ohio": [
        "Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron",
        "Dayton", "Parma", "Canton", "Youngstown", "Lorain",
        "Hamilton", "Springfield", "Kettering", "Elyria", "Lakewood"
    ],
    "Oklahoma": [
        "Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond",
        "Moore", "Midwest City", "Stillwater", "Enid", "Muskogee"
    ],
    "Oregon": [
        "Portland", "Eugene", "Salem", "Gresham", "Hillsboro",
        "Beaverton", "Bend", "Medford", "Springfield", "Corvallis",
        "Albany", "Tigard", "Lake Oswego", "Keizer", "Grants Pass"
    ],
    "Pennsylvania": [
        "Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading",
        "Scranton", "Bethlehem", "Lancaster", "Harrisburg", "Altoona",
        "York", "Wilkes-Barre", "Chester", "Williamsport", "Easton"
    ],
    "Rhode Island": [
        "Providence", "Cranston", "Warwick", "Pawtucket", "East Providence",
        "Woonsocket", "Coventry", "North Providence", "Cumberland"
    ],
    "South Carolina": [
        "Columbia", "Charleston", "North Charleston", "Mount Pleasant", "Rock Hill",
        "Greenville", "Summerville", "Goose Creek", "Hilton Head Island", "Florence"
    ],
    "South Dakota": [
        "Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown",
        "Mitchell", "Yankton", "Pierre", "Huron"
    ],
    "Tennessee": [
        "Memphis", "Nashville", "Knoxville", "Chattanooga", "Clarksville",
        "Murfreesboro", "Franklin", "Jackson", "Johnson City", "Bartlett",
        "Hendersonville", "Kingsport", "Collierville", "Cleveland", "Smyrna"
    ],    
    "Utah": [
        "Salt Lake City", "West Valley City", "Provo", "West Jordan", "Orem",
        "Sandy", "Ogden", "St. George", "Layton", "Taylorsville",
        "South Jordan", "Lehi", "Millcreek", "Clearfield", "Murray"
    ],
    "Vermont": [
        "Burlington", "South Burlington", "Rutland", "Essex Junction", "Barre",
        "Montpelier", "Winooski", "St. Albans"
    ],
    "Virginia": [
        "Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Newport News",
        "Alexandria", "Hampton", "Roanoke", "Portsmouth", "Suffolk",
        "Lynchburg", "Harrisonburg", "Charlottesville", "Danville", "Manassas"
    ],
    "Washington": [
        "Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue",
        "Kent", "Everett", "Renton", "Kirkland", "Yakima",
        "Bellingham", "Kennewick", "Federal Way", "Spokane Valley", "Redmond"
    ],
    "West Virginia": [
        "Charleston", "Huntington", "Parkersburg", "Morgantown", "Wheeling",
        "Weirton", "Fairmont", "Martinsburg", "Beckley"
    ],
    "Wisconsin": [
        "Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine",
        "Appleton", "Waukesha", "Oshkosh", "Eau Claire", "Janesville",
        "West Allis", "La Crosse", "Sheboygan", "Wauwatosa", "Fond du Lac"
    ],
    "Wyoming": [
        "Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs",
        "Sheridan", "Green River", "Evanston"
    ],
}

# ── Rate Limiting ────────────────────────────────────────────
DELAY_BETWEEN_REQUESTS = 1.5
DELAY_BETWEEN_SCRAPES  = 2.0
REQUEST_TIMEOUT        = 10
MAX_RETRIES            = 3

# ── Output ───────────────────────────────────────────────────
OUTPUT_CSV    = "usa_animal_shelters.csv"
PROGRESS_LOG  = "scraper_progress.log"
ERROR_LOG     = "scraper_errors.log"

# ── Scraping ─────────────────────────────────────────────────
MAX_PAGES_PER_CITY = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)