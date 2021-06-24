import os,soundfile
from pydub import AudioSegment
folders = ['Bark', 'Growling', 'Whimper', 'Bow-wow', 'Howl', 'Yip']
for type in folders:
    l = os.listdir(type+'/cropped/')
    a =set()
    for item in l:
        try:
            data, samplerate = soundfile.read(type + '/cropped/16bit/' + item)
            soundfile.write(type + '/cropped/16bit/' + item, data, samplerate, subtype='PCM_16')

        except Exception as e:
            print(e)
