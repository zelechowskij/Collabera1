import requests
import argparse
import logging
import sys
import json
import re

SECRET_FILE = "secret.json"
STATIC_URL = "https://api.macaddress.io/v1?output=json&search="
MAC_REG = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$"
#Change this to logging.INFO for more verbose output
LOGGING_LEVEL = logging.ERROR

logging.basicConfig(level=LOGGING_LEVEL, stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Get vendor from MAC Address')
parser.add_argument("mac", help='MAC address in one of the following formats XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX')
args = parser.parse_args()

class MacFormatError(ValueError):
    pass

class JsonKeyError(KeyError):
    pass

class ArgumentsKeyError(KeyError):
    pass

try:
    logger.info("Verifying MAC Address")
    if not re.match(MAC_REG, args.mac.lower()):
        raise MacFormatError

    logger.info(f"Opening {SECRET_FILE} json file")
    with open(SECRET_FILE) as jsonFile:
        secrets = json.load(jsonFile)
        jsonFile.close()

    logger.info("Retrieving API key")
    if not 'getMacAddr' in secrets and 'apiKey' in secrets['getMacAddr']:
        raise JsonKeyError
    else:
        API_KEY = secrets['getMacAddr']['apiKey']

    FINAL_URL = "https://api.macaddress.io/v1?output=vendor&search=" + args.mac 

    logger.info("Sending request")
    response = requests.get(FINAL_URL, headers={'X-Authentication-Token': API_KEY})

    if response.status_code == 200:
        print(response.text)
    else:
        raise requests.HTTPError(f'HTTP error\nStatus code:\t{response.status_code}\nResponse message:\t{response.text}')


except MacFormatError:
    logger.error("MAC Address in wrong format")
except FileNotFoundError:
    logger.error(f"file {SECRET_FILE} not found")
except JsonKeyError:
    logger.error(f"Error while trying to get information from {SECRET_FILE}")
except Exception as e:
    logger.error(e)
finally:
    logger.info("Closing the program")
    sys.exit()