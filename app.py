from flask import Flask,render_template,request,Response,redirect,flash,jsonify
import threading
import pyaudio
import wave
import speech_emotion as se
import os
from werkzeug.utils import secure_filename

DURATION = 10

otpValue = 0
ft = {"status":0,"emotion":""}

emoji_conversion = {'neutral': '😐',
                    'calm': '😐',
                    'happy': '😄',
                    'sad': '😢',
                    'angry': '😠',
                    'fearful': '😱',
                    'disgust': '😷',
                    'surprised': '😲'}


def clearaudios():
    try:
        cd = os.path.join(os.getcwd(),"static\\images\\audioIN")
        files = os.listdir(cd)
        for f in files:
            os.remove(os.path.join(cd, f))
    except:
        pass

def save_file(name,path,obj):
    f_path = os.path.join(path, name)
    if not os.path.exists(f_path):
        os.makedirs(f_path)
    for file in obj:
        filename = secure_filename(file.filename)  
        f_path1 = f_path
        f_path1 = os.path.join(f_path1, filename)
        if not os.path.exists(f_path1):
            file.save(f_path1)
        return filename

def getDevice():
    deviceList = []
    audio = pyaudio.PyAudio()
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0,numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            devicename = audio.get_device_info_by_host_api_device_index(0, i).get('name')
            #print("Input Device id ", i, " - ",devicename)
            deviceList.append(devicename)
    return deviceList
    

def setDevice():
    global ft

    while True:
        if ft["status"] == 1:
            Name ="audioFile"
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 512
            RECORD_SECONDS = DURATION
            audio = pyaudio.PyAudio()
            index = ft["index"]	
            ft["status"] = 2
            print("recording via index "+str(index))
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,input_device_index = index,
                            frames_per_buffer=CHUNK)
            print ("recording started")
            Recordframes = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                Recordframes.append(data)
            print("recording stopped")
            ft["status"] = 2
            stream.stop_stream()
            stream.close()
            audio.terminate()
            OUTPUT_FILENAME=Name+".wav"
            WAVE_OUTPUT_FILENAME=OUTPUT_FILENAME
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(Recordframes))
            waveFile.close()
            ft["status"] = 3
            print("audio file saved") 

            ft["emotion"] =se.predict_speaker_emotions("audioFile.wav")
            ft["status"] = 4
            print("audio file predicted")
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == "POST":
        return ""
    return render_template('home.html')

@app.route("/realtime",methods = ['get','post'])
def selectDevice():
    Dlist = getDevice()
    global ft
    if request.method == "GET":
        ft["status"] = 0
        return render_template('realTime.html')
    if request.method=="POST":
        resp = request.data.decode('utf-8')
        if("getdevice" in resp):return {"data":Dlist}
        if("sts" in resp):return ft
        if("index" in resp):
            index = int(resp.split(":")[1])
            ft["index"] = index
            ft["status"] = 1
            return {"data":1}
        return {"data":1}
@app.route('/form',methods=["get","post"])
def form():
    try:
        if request.method == 'POST':
            if 'audioFile' not in request.files:
                if request.data.decode('utf-8')=="check":
                    print("no file")
                    return jsonify({"status":"1"})                    
            else:
                clearaudios()
                imgFile = request.files.getlist("audioFile")
                a_path = os.path.join(os.getcwd(), 'static/images')
                imName = save_file("audioIN",a_path,imgFile)
                a_path = os.path.join(os.getcwd(), 'static/images/audioIN',imName)
                emotion = se.predict_speaker_emotions(a_path)
                print(emotion)
                return jsonify({"status":"0","emotion":emotion})
        else:
            return render_template("audioIn.html")


            #save_number(name,{"mobile":phone,"profile":i_path})
    except Exception as e:
        print("error:wrong format",e)
    return jsonify({"status":"1"})
########################################################################################
kwargs = {'port': 8080, 'threaded': True, 'use_reloader': False, 'debug': True}
if __name__ == '__main__':
    threading.Thread(target=setDevice).start()
    threading.Thread(target=app.run, daemon=True, kwargs=kwargs).start()  