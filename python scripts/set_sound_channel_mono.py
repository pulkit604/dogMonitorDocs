import os,soundfile
from pydub import AudioSegment
folders = ['Bark', 'Growling', 'Whimper', 'Bow-wow', 'Howl', 'Yip']
for type in folders:
    l = os.listdir(type+'/cropped/16bit/')
    a =set()
    for item in l:
        try:
            sound = AudioSegment.from_file(type + "/cropped/16bit/" + item)
            sound = sound.set_channels(1)
            sound.export(type + '/cropped/16bit/' + item, format="wav")

        except Exception as e:
            print(e)
