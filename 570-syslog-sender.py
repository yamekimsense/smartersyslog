import socket
import requests
import json

accessToken = ""  # Bot's access token
host = "https://api.ciscospark.com/v1/"
headers = {"Authorization": "Bearer %s" % accessToken, "Content-Type": "application/json"}


UDP_IP = "0.0.0.0"
UDP_PORT = 514

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(5000)
    print (data)
    print (type(data))

    data = str (data, 'utf-8')
    print (type(data))

    response = requests.get(host + "rooms/", headers=headers)

#print (response.text)

    json_data = json.loads(response.text)
    items = json_data["items"]
    number = len(items)

    for i in range(0, number):
        #print (items[i])

#get the room ID
        room_id = items[i]['id']
        print (room_id)

#send the message to each room
        payload = {"roomId": room_id, "text": data}
        response = requests.request("POST", host + "messages/", data=json.dumps(payload), headers=headers)

        print ("PRINT", room_id, data)