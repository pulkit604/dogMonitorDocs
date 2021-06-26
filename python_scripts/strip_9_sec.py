import os,soundfile
from pydub import AudioSegment
folders = ['Bark', 'Growling', 'Whimper', 'Bow-wow', 'Howl', 'Yip']
for type in folders:
    l = os.listdir(type+'/cropped/16bit/')
    for item in l:
        try:
            sound = AudioSegment.from_file(type + "/cropped/16bit/" + item)
            extract = sound[0:9000]
            extract.export(type + '/cropped/16bit/' + item, format="wav")

        except Exception as e:
            print(e)
