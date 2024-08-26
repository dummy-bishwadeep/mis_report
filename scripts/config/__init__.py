"""
This file exposes configurations from config file and environments as Class Objects
"""
import shutil

# from dotenv import load_dotenv

# load_dotenv()
import os.path
import sys
from configparser import BasicInterpolation, ConfigParser


class EnvInterpolation(BasicInterpolation):
    """
    Interpolation which expands environment variables in values.
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)

        if not os.path.expandvars(value).startswith("$"):
            return os.path.expandvars(value)
        else:
            return



try:
    config = ConfigParser(interpolation=EnvInterpolation())
    config.read("conf/application.conf")
except Exception as e:
    print(f"Error while loading the config: {e}")
    print("Failed to Load Configuration. Exiting!!!")
    sys.stdout.flush()
    sys.exit()

class DBConf:
    KAIROS_URI = config.get("KAIROS_DETAILS", "kairos_uri")
    KAIROS_USERNAME = config.get("KAIROS_DETAILS", "kairos_username")
    KAIROS_PASSWORD = config.get("KAIROS_DETAILS", "kairos_password")
    KAIROS_METRIC = config.get("KAIROS_DETAILS", "kairos_metric")
    # if not KAIROS_URI:
    #     print("Error, environment variable KAIROS_URI not set")
    #     sys.exit(1)

