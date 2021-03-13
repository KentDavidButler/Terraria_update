"""
Main file that runs the entire Terraria Server Update
This file imports Terraria_Website.py and Local_Server.py
from the local directory.
This program (when finished) will run in a loop but only
trigger once a day to check the Terraria website for updates.
It will check if the Terraria server is running ever five mins.
"""
from datetime import datetime
import time
import logging
import asyncio

import Terraria_Website as site
import Local_Server as serv

# check site for updates at 2AM everyday
now = datetime.now()
check_site_for_update_low = now.replace(hour=2, minute=0, second=0, microsecond=0)
check_site_for_update_high = now.replace(hour=2, minute=5, second=0, microsecond=0)


# sleep timer used to delay looping through code
sleep_timer = 60
server_subprocess = "na"

if __name__ == "__main__":
    logging.basicConfig(format=("%(asctime)s --- %(levelname)s --- %(message)s"),
                        datefmt=("%Y-%m-%d %H:%M:%S"),
                        level=logging.DEBUG)

    local_version = serv.get_latest_installed_version()
    site_version = site.get_version()
    site_version = int(site_version[-4:])

    logging.debug('Python Script is starting')
    logging.debug('The Local Terraria version is %s', local_version)
    logging.debug('The Site Version of Terraria is %s', site_version)

    while True:

        now = datetime.now()
        if now > check_site_for_update_low and now < check_site_for_update_high: 
            "Checking Site Version - Should occure Once between 2am and 2:05am Eastern"
            logging.debug('Checking Site Version')
            site_version = site.get_version()
            site_version = int(site_version[-4:])
            logging.debug('The Site Version of Terraria is %s', site_version)

            logging.debug('Checking Local Version')
            local_version = serv.get_latest_installed_version()
            logging.debug('The Local Version of Terraria is %s', local_version)

        if site_version > local_version:
            "download and install latest version"
            logging.debug('Site Version is higher than local version')
            logging.debug('Updating Local Version of Terraria')

            site.download_latest_version()
            serv.extract_zip()

            if serv.is_server_running():
                logging.debug('Saving and stopping Server')
                server_subprocess.stop_ter_serv

            local_version = serv.get_latest_installed_version()

        "time to check if local server is running"
        logging.debug('Checking to see if the server is running')
        if serv.is_server_running() is False:
            logging.debug('Starting the local server: %s', server_subprocess)
            server_subprocess = serv.start_ter_serv(local_version)
        else:
            logging.debug('The Server is running: %s', server_subprocess)

        # server_log = asyncio.run(serv.get_server_log(server_subprocess))
        # logging.debug(server_log)
        time.sleep(sleep_timer)
        logging.debug('Looping back over script')
