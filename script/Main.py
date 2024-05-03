from datetime import datetime
from time import sleep

import winsound

from Database import Database
from PinnacleAPI import PinnacleAPI

pinnacle = PinnacleAPI()

num = 1
while True:
    pinnacle.update_database()
    print("times ran:" + str(num))
    num += 1
    sleep(pinnacle.TIME_BETWEEN_CALLS)
