from pydub import AudioSegment
import os
import pandas as pd

folders = ['Bark', 'Growling', 'Whimper', 'Bow-wow', 'Howl', 'Yip']
for type in folders:
    l = os.listdir(type)
    for item in l:
        try:
            name_parts = item.split('.')
            part_one   = name_parts[0].split('_')
            st         = part_one[-3]
            et         = part_one[-1]
            song = AudioSegment.from_file(type + '/'+ item)
            extract = song[int(st)*1000:int(et)*1000]
            extract.export(type + '/cropped/' + item, format="wav")
        except Exception as e:
            print(e)
