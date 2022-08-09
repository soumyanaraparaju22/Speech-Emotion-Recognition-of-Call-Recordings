# Speech-Emotion-Recognition-of-Call-Recordings

Recently, increasing attention has been directed to the study and recognition of the emotional
content of speech signals. It has become necessary to know the emotions of speakers to
identify their current situations and moods. Therefore, many systems are being proposed to
identify the emotional content of a spoken utterance. These system can be categorized into
systems focusing on deriving emotion from text and from voice. This work focuses on later
approach. During calls, it is difficult to recognize the emotions of the speakers in order to
assist or help them if needed.
In our project, Speech Emotion Recognition of Call Recordings the emotions of the callers
are identified using the recorded calls.Existing Speech Emotion Recognition Systems identify
emotions of a single speaker. Unlike the regular Speech Emotion Recognition Systems, our
system recognizes multiple speakers’ emotions that are present in a single recording.Major
steps involved in speech emotion recognition are speaker diarization, feature extraction and
classification.Speaker diarization is the process of portioning an input audio stream into
homogeneous segments according to the speaker’s identity using segmentation.
Later these segments are joined in clustering phase to generate continuous voice of individual
speakers. In the feature extraction step we extract features viz. signal, energy, zero cross rate
and pitch from the speech signals using MFCC approach. These features are given as input to
build CNN model. In classification step the input is classified into one of seven emotions i.e
Surprise, Happy, Neutral,Disgust, Angry, Fear and Sad.RAVDESS dataset containing voice
samples of 24 actors was used to train and test the built model. The System on recognizing or
classifying displays the emotion of the respective speaker. The accuracy of this model is
86%. Speech Emotion Detection (SED) system was developed by hosting this model on on
flask as a web application. This model can be used in call centers for feedback purposes,
crime investigations, suicide prevention etc. In future this model can be further extended to
consider text part of the voice for better emotion recognition.
