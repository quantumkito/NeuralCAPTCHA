import os
import librosa
import numpy as np

audio_path = "AudioCaptchas/"
num_classes = 10
num_mfcc = 13
max_len = 128

def load_audio(file_path):
    audio, sr = librosa(file_path, sr = 44100)
    mfccs = librosa.feature.mfcc(y = audio, sr = sr, n_mfcc = num_mfcc)
    mfccs = (mfccs - np.mean(mfccs)) / np.std(mfccs)
    mfccs = mfccs[:, :max_len] if mfccs.shape[1] > max_len else np.pad(mfccs, ((0, 0), (0, max_len - mfccs.shape[1])), mode='constant')
    return mfccs

label_map = {label: idx for idx, label in enumerate(sorted(os.listdir(audio_path)))}

X = []
y = []

for filename in os.listdir(audio_path):
    file_path = os.path.join(audio_path, filename)
    mfccs = load_audio(file_path)
    label = filename.split('_')[0]

    X.append(mfccs)
    y.append(label_map[label])

X = np.array([x[:max_len] for x in X])
X = (X - np.mean(X)) / np.std(X)

