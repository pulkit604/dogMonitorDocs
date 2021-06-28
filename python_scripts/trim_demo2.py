from pydub import AudioSegment
import os
import pandas as pd

folders = ['Bark', 'Growling', 'Whimper', 'Bow-wow', 'Howl', 'Yip']
dl = []
for type in folders:
    l = os.listdir(type)
    for item in l:
        try:
            name_parts = item.split('.')
            part_one   = name_parts[0].split('_')
            st         = part_one[len(part_one)-1]
            et         = name_parts[1].split('_')[2]
            dl.append([type, name_parts[0].split('_')[0], st, et])
            song = AudioSegment.from_file(type + '/'+ item)
            extract = song[int(st)*1000:int(et)*1000]
            extract.export(type + '/cropped/' + item, format="wav")
        except Exception as e:
            print(e)

df = pd.DataFrame(dl)
writer = pd.ExcelWriter('updated.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='First', index=False)
writer.save()
