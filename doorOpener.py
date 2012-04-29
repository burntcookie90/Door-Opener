import serial
import time
import imaplib, re
import pyaudio
import wave
import sys

ser = serial.Serial('/dev/ttyACM0')
print "Starting on " +ser.portstr;
conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
conn.login('USERNAME','PASSWORRD')
oldUnreadCount = 0
while (True):
	try:
		unreadCount = int(re.search("UNSEEN (\d+)", conn.status("[Gmail]/Starred", "(UNSEEN)")[1][0]).group(1))
	except conn.abort:
		conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
		conn.login('USERNAME','PASSWORRD')
		unreadCount = int(re.search("UNSEEN (\d+)", conn.status("[Gmail]/Starred", "(UNSEEN)")[1][0]).group(1))
	except IOError, e:
		if e.errno == 101:
			print "Network Error"
			time.sleep(5)
	if(unreadCount > oldUnreadCount):
		print str(unreadCount-oldUnreadCount) + " new mails!"
		ser.write("M")
		time.sleep(2)
		chunk = 1024

		wf=wave.open('welcome_home.wav','rb')
		p=pyaudio.PyAudio()
		# open stream
		stream = p.open(format =
                		p.get_format_from_width(wf.getsampwidth()),
		                channels = wf.getnchannels(),
		                rate = wf.getframerate(),
		                output = True)

		# read data
		data = wf.readframes(chunk)
		while data != '':
#		print "lol"
   			stream.write(data)
   			data = wf.readframes(chunk)

		stream.close()
		p.terminate()
	else:
		print "no new mail :("
		ser.write("N")
	oldUnreadCount = unreadCount
	time.sleep(1)
