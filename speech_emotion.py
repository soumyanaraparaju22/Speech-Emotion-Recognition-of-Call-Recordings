import os 
import shutil

import numpy as np

import warnings
warnings.filterwarnings("ignore")

import soundfile
import librosa , librosa.display
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization')

import joblib
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
loaded_model = tf.keras.models.load_model("saved_model.hdf5")

Diarized_speakers_Path = "Diare"

def diarize_audio(file):
    print("checking the audio files")
    y , sr = librosa.load(file, offset=0) 
    if float(librosa.get_duration(y,sr))<4.5:
        y, index = librosa.effects.trim(y, top_db=50, frame_length=128, hop_length=32)
        soundfile.write(os.path.join(Diarized_speakers_Path,f"speaker_0.wav"), y, sr)

    print("Diarizing the speakers audio")
    diarization = pipeline(file)
    speakers = [[] for _ in diarization.labels()]
    for turn, _, speaker in diarization.itertracks(yield_label=True,):
        print(turn.start,turn.end,speaker)
        Off_set = turn.start
        Duration = turn.end - turn.start
        Signal , sr = librosa.load(file, offset=Off_set,duration=Duration) 
        speakers[int(speaker[-2:])].append(Signal)
    for j,i in enumerate(speakers):
        if len(i)>1:
            S = np.hstack(i)
            soundfile.write(os.path.join(Diarized_speakers_Path,f"speaker_{j}.wav"), S, sr)
        elif len(i)==1:
            soundfile.write(os.path.join(Diarized_speakers_Path,f"speaker_{j}.wav"), i[0], sr)


def predict_emotion(file):
    print("predicting emotions")
    Signal, sampling_rate = librosa.load(file)
    temp = []
    energy = librosa.feature.rms(y=Signal)
    temp.append(energy.mean())

    zcr = librosa.feature.zero_crossing_rate(Signal)
    temp.append(zcr.mean())

    S = np.abs(librosa.stft(Signal))
    pitches, magnitudes = librosa.piptrack(S=S)
    temp.append(pitches.mean())

    mfccs = librosa.feature.mfcc(y=Signal)
    temp.extend(list(mfccs.mean(axis=1)))
    temp = np.array(temp)
    scale = joblib.load("scaling_object.sav")
    temp = scale.transform(np.array(temp).reshape(1, -1))
    x = np.reshape(temp,(1,temp.shape[1],1))
 
    predictions = loaded_model.predict(x)
        
    label_conversion = {'0': 'neutral 😐',
                        '1': 'calm 😐',
                        '2': 'happy 😄',
                        '3': 'sad 😢',
                        '4': 'angry 😠',
                        '5': 'fearful 😱',
                        '6': 'disgust 😷',
                        '7': 'surprised 😲'}



    for key, value in label_conversion.items():
        if int(key) == np.argmax(predictions,axis=-1):
            label = value
    return label

def predict_speaker_emotions(file):
    for i in os.listdir(Diarized_speakers_Path):
        try:
            os.remove(os.path.join(Diarized_speakers_Path,str(i)))
        except PermissionError:
            try:
                shutil.rmtree(str(i))
            except:
                print("clear the storage manualy")

    diarize_audio(file)


    res = []
    for speaker_file in os.listdir(Diarized_speakers_Path):
        res.append((speaker_file,predict_emotion(os.path.join(Diarized_speakers_Path,speaker_file))))
    
    result = "</br>"
    for i,j in res:
        result += i.split(".")[0]+" emotion: "+j+"</br>"
    
    print("processing is done output will be given soon")

    return result



if __name__ == "__main__":
    print(predict_speaker_emotions("RAVDESS/Actor_01/03-01-05-01-01-01-01.wav"))

