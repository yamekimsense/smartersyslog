import time, datetime, requests, json, paramiko
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from flask import Flask
from flask import request
from requests_toolbelt.multipart.encoder import MultipartEncoder
#pip install requests-toolbelt

botEmail = "smartsyslog@webex.bot"
accessToken = ""  # Bot's access token
host = "https://api.ciscospark.com/v1/"
headers = {"Authorization": "Bearer %s" % accessToken, "Content-Type": "application/json"}

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_tasks():
    print ("=============================================================")
    print (datetime.datetime.now())

    email = request.json.get('data').get('personEmail')
    print ("email =", email)

    if email == "smartsyslog@webex.bot":
        return ("")

    messageId = request.json.get('data').get('id')
    print ("all == ", request.json.get('data'))
    room = request.json.get('data').get('roomId')
    print ("room_id == ", room)

    response = requests.get(host + "messages/" + messageId, headers=headers)
    key = response.json().get('text')
    print ("keyword length ==", len(key))
    print ("keyword is == ", key)

    ### for show tech command

    if (key == "show tech"):

        payload = {"roomId": room, "text": "show tech is too long. Sorry!"}
        response = requests.request("POST", "https://api.ciscospark.com/v1/messages/",
                                    data=json.dumps(payload), headers=headers)
        return ("")

    ### for other command

    if (key != "show log"):
        print ("-------------- SSH other Paramiko ---------------")

        ip = "192.168.30.251"
        username = "cisco"
        password = "cisco"

        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        remote_conn_pre.connect(ip, port=22, username=username,
                                password=password,
                                look_for_keys=False, allow_agent=False)

        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print ("conn= ", output)

        remote_conn.send("terminal length 0\n")
        time.sleep(.5)
        output = remote_conn.recv(65535)

        remote_conn.send(key + "\n")
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print ("show result is =", output)
        print (type(output))
        print (str(output, 'utf-8'))
        print (type(str(output, 'utf-8')))
        result = str(output, 'utf-8')

        ###
        payload = {"roomId": room, "text": result}
        response = requests.request("POST", "https://api.ciscospark.com/v1/messages/",
                                    data=json.dumps(payload), headers = headers)



### for other command

    if (key == "show log"):

        print ("-------------- SSH LOG LOG LOG Paramiko ---------------")

        ip = "192.168.30.251"
        username = "cisco"
        password = "cisco"

        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        remote_conn_pre.connect(ip, port=22, username=username,
                                password=password,
                                look_for_keys=False, allow_agent=False)

        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print ("conn= ", output)

        remote_conn.send("terminal length 0\n")
        time.sleep(.5)
        output = remote_conn.recv(65535)

        remote_conn.send(key + "\n")
        time.sleep(.5)
        output = remote_conn.recv(65535)
        print ("show result is =", output)
        print (type(output))
        print (str(output, 'utf-8'))
        print (type(str(output, 'utf-8')))
        result = str(output, 'utf-8')

        f = open ("log.txt", 'w')
        f.write (result)
        f.close()

        #payload = {"roomId": room, "text": "see the text file for the log", "files": "/root/test.txt"}
        #response = requests.request("POST", "https://api.ciscospark.com/v1/messages/",
        #                            data=json.dumps(payload), headers = headers)

        m = MultipartEncoder({'roomId': room,
                              'text': 'show log was attached',
                              'files': ('log.txt', open('log.txt', 'rb'),
                                        'text/plain')})

        r = requests.post('https://webexapis.com/v1/messages', data=m,
                          headers={'Authorization': "Bearer %s" % accessToken,
                                   'Content-Type': m.content_type})

        print (r.text)

    return ("")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=True)
