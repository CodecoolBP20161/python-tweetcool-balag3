import argparse
import ipaddress
import requests
import json
import datetime
import subprocess



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

# Logic starts here... somewhere..

my_route = server["address"]+"/tweet"
user = 'code'
# y = subprocess.check_output('whoami')


def get_tweets():
    get_it = requests.get(my_route)
    to_json = get_it.json()
    return to_json


def tweet_formatter():
    json_data = get_tweets()
    for i in json_data:
        print("")
        print(i['poster'], "<" + str(datetime.datetime.utcfromtimestamp(int(i['timestamp']))) + ">:", i['content'])
    print("")


def post_tweet(message):
    message = str(message)
    payload = {"content": message, "poster": user}
    requests.post(my_route, json=payload)


def menu():
    print('Available commands : \n refresh : Refresh the lates tweets.\n exit : Exit the program.\n post : Post a tweet.')
    command = input('command: ')
    return command

tweet_formatter()
while True:
    try:
        command = menu()
        if command == 'refresh':
            tweet_formatter()
        elif command == 'exit':
            exit()
        elif command == 'post':
            message = input('Type your message: ')
            post_tweet(message)
            tweet_formatter()
    except EOFError:
        exit()
    except KeyboardInterrupt:
        exit()
