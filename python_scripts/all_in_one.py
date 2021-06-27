import pygame
import pyaudio
import wave
import requests
import time
from pyfcm import FCMNotification
'''
1. Teil Aufnehmen
'''
def record():

	form_1 = pyaudio.paInt16 # 16-bit resolution
	chans = 1 # 1 channel
	samp_rate = 44100 # 44.1kHz sampling rate
	chunk = 4096 # 2^12 samples for buffer
	record_secs = 9 # seconds to record
	dev_index = 2 # device index found by p.get_device_info_by_index(ii)
	wav_output_filename = 'test1.wav' # name of .wav file

	audio = pyaudio.PyAudio() # create pyaudio instantiation

	# create pyaudio stream
	stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
	                    input_device_index = dev_index,input = True, \
	                    frames_per_buffer=chunk)
	frames = []
	# loop through stream and append audio chunks to frame array
	for ii in range(0,int((samp_rate/chunk)*record_secs)):
	    data = stream.read(chunk)
	    frames.append(data)

	print("finished recording")

	# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# save the audio frames as .wav file
	wavefile = wave.open(wav_output_filename,'wb')
	wavefile.setnchannels(chans)
	wavefile.setsampwidth(audio.get_sample_size(form_1))
	wavefile.setframerate(samp_rate)
	wavefile.writeframes(b''.join(frames))
	wavefile.close()


'''
2. Teil Api
'''
def call_api():
    print(':::::      Calling API      ::::::::::::')
    return requests.get("http://127.0.0.1:5000/check").json()




'''
3. Teil Abspielen
'''
def play():
	pygame.mixer.init()
	pygame.mixer.music.load("calm_scrott.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
	    continue


'''
4. Push Not
'''
def send_push():
	push_service = FCMNotification(api_key="AAAAzxLdr8I:APA91bGS8izl4MF_ghd0DrIc36stoufOtqtv_jfHzzwH46ANprHSzpX9Rs4BwekCM2wSFX8SYtdFnjzPX5sQuePDyJvAFXdLmWAzhzcNyYj3MxZN673PtFDgT5mMwOL0kNrL2Q0OXkvo")
	registration_id = "diHtRAOs_PoatAQk04afp8:APA91bFF_sg4dYJP2Tst_4JrTjFDcQIBn9x49zGce5L5gicQzDtzK8l5UpF8JD6iLhavf6uvqJmcClxZHJZcKyD2Q8pmCuVmwh-0xvcC1b5kO97oRLKLAs63YGvJV8FwiXfqGH4tDrJC"
	message_title = "Dog is sad"
	message_body = "Hi john, dog is sad and we can't help. do something"
	result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
times=0
while True:
    print(":::::: Recording ::::::")
    record()
    time.sleep(3)
    res = call_api()
    print('api response: ', res)
    time.sleep(3)
    if res['result'] == 'True':
        print(":::::: Playing calm music  ::::::")
        times=times+1
        play()
        time.sleep(3)
    if times==2:
        print(":::::  Sending Push Notification  ::::::")
        send_push()
        exit()
