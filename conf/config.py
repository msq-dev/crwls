import os
from pathlib import Path
import configparser

config_dir = Path(__file__).parent.resolve()
config_ini = Path(config_dir) / "config.ini"

config = configparser.ConfigParser()
config.read(config_ini)

environments = {
    "/Users/bmpotatoe": "DEV"
}

COLUMNS = config["DEFAULT"]["columns"]
MAIL_MODE = config["DEFAULT"].getboolean("mailmode")
ENV = environments[os.environ["HOME"]]

APP = config[ENV]["app"]
URLS_LIST = config[ENV]["urlslist"]
OUTPUT_PATH = config[ENV]["outputpath"]
CHANGES_PATH = config[ENV]["changespath"]
GMAIL_USER = config[ENV]["gmailuser"]
GMAIL_PASSWORD = config[ENV]["gmailpassword"]
