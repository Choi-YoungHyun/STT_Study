"""
필요한 라이브러리
pytube
openai-whisper
ffmpeg

"""
from datetime import datetime
import whisper
import os
import subprocess

FFMPEG = "C:\\ffmpeg\\bin\\ffmpeg.exe"

def splitAudio(Model_Result,input_File):
    for i,segment in enumerate(Model_Result):
        command = [
            FFMPEG,
            "-y", 
            "-i", input_File, 
            "-ss", str(segment["start"]), 
            "-to", str(segment["end"]), 
            "-hide_banner", 
            "-loglevel", 
            "error",
            f"wavs/audio{i}.wav" 
        ]
        subprocess.run(command)

model = whisper.load_model("small")


print(os.getcwd())
print(os.path.join(os.getcwd(), "output.mp3"))
print("================================")
print(f"현재 파일 생성 유무   :       {os.path.isfile('output.mp3')}")


print('Model Start!')
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
result = model.transcribe("output.mp3")
print('Model End!')
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


print('SPlit wav START!')
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
splitAudio(result["segments"],"output.mp3")
print('SPlit wav END!')
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

