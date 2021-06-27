from flask import Flask
import tensorflow as tf
import os,json
app = Flask(__name__)

def decode_audio(audio_binary):
  audio, _ = tf.audio.decode_wav(audio_binary)
  return tf.squeeze(audio, axis=-1)
def get_label(file_path):
  parts = str(file_path).split(os.path.sep)
  if tf.strings.split(file_path, '/')[0] == 'Yip' or tf.strings.split(file_path, '/')[0] == 'Whimper':
    return 'yes'
  return 'no'

def get_waveform_and_label(file_path):
  label = get_label(file_path)
  audio_binary = tf.io.read_file(file_path)
  waveform = decode_audio(audio_binary)
  return waveform, label

def get_spectrogram(waveform):
  # Padding for files with less than 16000 samples
  #zero_padding = tf.zeros([16000] - tf.shape(waveform), dtype=tf.float32)

  # Concatenate audio with padding so that all audio clips will be of the
  # same length
  waveform = tf.cast(waveform, tf.float32)
  equal_length = tf.concat([waveform], 0)
  spectrogram = tf.signal.stft(
      equal_length, frame_length=255, frame_step=128)
  print(spectrogram.shape)
  spectrogram = tf.abs(spectrogram)

  return spectrogram

def get_spectrogram_and_label_id(audio, label):
  commands = ['yes', 'no']
  spectrogram = get_spectrogram(audio)
  spectrogram = tf.expand_dims(spectrogram, -1)
  label_id = 1#tf.argmax(label == commands)
  return spectrogram, label_id

def preprocess_dataset(files):
    files_ds = tf.data.Dataset.from_tensor_slices(files)
    output_ds = files_ds.map(get_waveform_and_label, num_parallel_calls=None)
    output_ds = output_ds.map(
        get_spectrogram_and_label_id,  num_parallel_calls=None)
    return output_ds

@app.route('/check')
def check_audio():
    sample_file = 'test1.wav'
    sample_ds = preprocess_dataset([str(sample_file)])
    model=tf.keras.models.load_model('saved_model')
    for spectrogram, label in sample_ds.batch(1):
        prediction = model(spectrogram)
        smax=tf.nn.softmax(prediction[0]).numpy()
        print(smax)
        return json.dumps({'result': str((smax[1] - smax[0])<0.21)})
