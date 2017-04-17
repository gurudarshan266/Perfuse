from db_utils import chunk_database
from constants import *
import time

class DiskBalancer():

    def __init__(self,max_cap):
        self.max_cap = max_cap

    def start(self):
        db = chunk_database()
        sz = db.get_total_size()

        if sz < TRIGGER_LEVEL*self.max_cap:
            pass

        time.sleep(DISK_BALANCER_PERIOD)


d = DiskBalancer(10*1024*1024)
d.start()