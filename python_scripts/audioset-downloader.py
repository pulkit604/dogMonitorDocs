import pafy, time, ffmpy
from pathlib import Path
import pandas as pd
import soundfile as sf
from concurrent.futures import ProcessPoolExecutor

file = pd.read_excel('c.xlsx')

category    = file.iloc[:,0].tolist()[2:]
audio_ids = file.iloc[:,1].tolist()[2:]
audio_starts   = file.iloc[:,2].tolist()[2:]
audio_ends  = file.iloc[:,3].tolist()[2:]
#audio_labels = file.iloc[:,3].tolist()[2:]

com_link = 'https://www.youtube.com/watch?v='
def map_func(i, audio_id, audio_start, audio_end, category):
    dl_link = com_link + audio_id
    start_time = audio_start
    end_time = audio_end
    try:
        video = pafy.new(dl_link)
        tile  = video.title
        bestaudio = video.getbestaudio()
        file_path = "./" + category +  '/' + f'{audio_id}_start_{start_time}_end_{end_time}{bestaudio.extension}'
        print(f"start to download {dl_link}")
        audioname = bestaudio.download(filepath=str(file_path))
        print(f"end to download {dl_link}")
        extension = bestaudio.extension

        if extension not in ['wav']:
            xindex    = audioname.find(extension)
            audioname = audioname[0:xindex]
            conv2wav  = ffmpy.FFmpeg(
                inputs  = {audioname + extension:None},
                outputs = {audioname + '.wav':None}
            )
            conv2wav.run()
            file_to_rem = Path(audioname + extension)
            file_to_rem.unlink()

        file = audioname + '.wav'
        data, sample_rate = sf.read(file)

        total_time  = len(data)/sample_rate
        start_point = sample_rate * start_time
        end_point   = sample_rate * end_time

        sf.write('./audioset/' + audio_id + '.wav', data[start_point:end_point], sample_rate)
        #sf.write(file, data[start_point:end_point], sample_rate)
        file_to_rem2 = Path(file)
        file_to_rem2.unlink()

    except Exception as e:
        print(e)


with ProcessPoolExecutor(8) as executor:
    executor.map(map_func, range(len(audio_ids)), audio_ids, audio_starts, audio_ends, category,  timeout=10)
