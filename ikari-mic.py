#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

import os
import pyaudio
import subprocess
import wave
import numpy as np
from datetime import datetime

IKARI_HOST=os.environ["IKARI_HOST"]
IKARI_PORT=os.environ["IKARI_PORT"]
API_KEY=os.environ["EMPATH_KEY"]

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 44100
RATE = 11025
RECORD_SECONDS = 2

# threshold = 0.01
# threshold = 0.03
threshold = 0.7

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

cnt = 0

while True:
    data = stream.read(chunk)
    x = np.frombuffer(data, dtype="int16") / 32768.0
    if x.max() > threshold:
        print("x.max = {}".format(x.max()))
        # filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"
        filename = "ikari.wav"
        print(cnt, filename)

        all = []
        all.append(data)
        for i in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
            data = stream.read(chunk)
            all.append(data)
        data = b''.join(all)

        out = wave.open(filename,'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data)
        out.close()

        print("Saved.")
	    
        cmd = "curl http://{}:{} -X POST -F \"file=@./ikari.wav\" -F \"api-key={}\"".format(IKARI_HOST, IKARI_PORT, EMPATH_KEY)
        subprocess.call(cmd, shell=True)
        print(cmd)
        
        cnt += 1
    if cnt > 5:
        # break
        cnt = 0

stream.close()
p.terminate()
