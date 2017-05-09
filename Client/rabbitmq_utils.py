import pika
import json
from geoip import geolite2
from time import sleep
import requests

SCALEDOWN_FACTOR = 1000
FREEGEOPIP_URL = 'http://freegeoip.net/json'

def get_location2(ip_addr):
    match = geolite2.lookup(ip_addr)
    if match is not None:
        return list(match.location)
    else:
        return [0.0,0.0]

def get_location(ip_addr):
    url = '{}/{}'.format(FREEGEOPIP_URL, ip_addr)
    response = requests.get(url)
    response.raise_for_status()
    rj = response.json()
    return [ float(rj["latitude"]) , float(rj["longitude"]) ]


def add_to_transfer_queue(sender_ip,receivers_ip,n):
    connection = pika.BlockingConnection(pika.ConnectionParameters('152.7.99.61'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    n = int(n/SCALEDOWN_FACTOR)

    sender_loc = get_location(sender_ip)
    receivers_loc = [ get_location(x) for x in receivers_ip ]

    m = [{"sender":sender_loc, "receiver":receivers_loc}]
    s = json.dumps(m)
    print s

    s2 = '[ {"sender":[23.795398,72.597656],\
                "receiver":[[8.309341,15.644531],[-27.459539,126.035156]]\
                } ]'
    print s2

    for i in range(n):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=s)
        sleep(1.1)

    print(" [x] Sent 'Hello World!'")

    connection.close()

add_to_transfer_queue("152.7.99.61",["24.163.44.95","52.56.177.147","52.76.232.13"],20000)
