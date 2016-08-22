import argparse
import ipaddress
import requests
import json
import datetime



parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host",
                    help="IP address of the Tweetcool server",
                    default='127.0.0.1')  # Equals 'localhost'
parser.add_argument("-P", "--port",
                    help="Post used by the Tweetcool server",
                    type=int,
                    default=9876)
args = parser.parse_args()

try:
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])


def tweet_formatter(json_data):
    for i in json_data:
        print(i['poster'], "<" + str(datetime.datetime.utcfromtimestamp(int(i['timestamp']))) + ">:", i['content'])

# Logic starts here... somewhere..
my_route = server["address"]+"/tweet"
# payload = {"content": "Do. Or do not. There is no try.", "poster": "Yoda"}
# post_it = requests.post('http://127.0.0.1:9876/tweet', json=payload)
get_it = requests.get(my_route)
x = get_it.json()
tweet_formatter(x)
