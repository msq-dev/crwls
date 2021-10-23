import os
from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation

config_dir = Path(__file__).parent.resolve()
config_ini = Path(config_dir) / "config.ini"

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(config_ini)

environments = {
    "/Users/bmpotatoe": "DEV"
}

COLUMNS = config["DEV"]["columns"]
MAIL_MODE = config["DEFAULT"].getboolean("mailmode")
# ENV = environments[os.environ["HOME"]]
ENV = Path.home()

APP = config[ENV]["app"]
URLS_LIST = config[ENV]["urlslist"]
OUTPUT_PATH = config[ENV]["outputpath"]
CHANGES_PATH = config[ENV]["changespath"]
GMAIL_USER = config[ENV]["gmailuser"]
GMAIL_PASSWORD = config[ENV]["gmailpassword"]
