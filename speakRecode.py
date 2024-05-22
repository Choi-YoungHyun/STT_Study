import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from pytube import YouTube
from datetime import datetime
import whisper
import os
import subprocess

# ffmpeg 경로 설정 (ffmpeg이 설치된 경로로 대체) + 모델 불러오기 
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
FFMPEG = "C:\\ffmpeg\\bin\\ffmpeg.exe"

print('11111111111111111111111111111111111')
MODEL = whisper.load_model("small")
print('Model Loading OK!')
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

############ 전역 변수 ######################################
DUARTION = 10  # 녹음 시간(초)
SAMPLE_RATE = 44100  # 샘플링 속도
GAIN_DB = 30  # 볼륨을 증폭할 데시벨 값   (50 미만 추천)
WAV_FILE = "output.wav"
MP3_FILE = "output.mp3"


amplified_wav_filename = "amplified_output.wav"


def record_audio(duration, sample_rate):
    print("녹음을 시작합니다...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()  # 녹음 완료까지 대기
    print("녹음이 완료되었습니다.")
    print(recording)
    return recording

def save_as_wav(recording, sample_rate, filename):
    write(filename, sample_rate, recording)
    print(f"{filename} 파일이 저장되었습니다.")

def amplify_audio(input_wav, output_wav, gain_dB):
    audio = AudioSegment.from_wav(input_wav)
    amplified_audio = audio + gain_dB
    amplified_audio.export(output_wav, format="wav")
    print(f"{output_wav} 파일이 저장되었습니다 (증폭됨).")

def convert_wav_to_mp3(wav_filename, mp3_filename):
    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3")
    print(f"{mp3_filename} 파일이 저장되었습니다.")


def convert_youTube(youtubeURL):
    video = YouTube(youtubeURL)
    video.streams.filter(only_audio=True).first().download(output_path='.', filename= MP3_FILE)


def splitAudio(Model_Result,input_File):
    for i,segment in enumerate(Model_Result):
        command = [
            FFMPEG,
            "-y", 
            "-i", input_File, 
            "-ss", segment["start"], 
            "-to", segment["end"], 
            "-hide_banner", 
            "-loglevel", 
            "error",
            f"wavs/audio{i}.wav" 
        ]
    subprocess.run(command)






standard = input("1 or 2")

if(standard == "1"):
    # 녹음 시작
    recording = record_audio(DUARTION, SAMPLE_RATE)
    # WAV 파일로 저장
    save_as_wav(recording, SAMPLE_RATE, WAV_FILE)
    #소리 증폭 
    amplify_audio(WAV_FILE, amplified_wav_filename, GAIN_DB)
    # MP3 파일로 변환
    convert_wav_to_mp3(amplified_wav_filename, MP3_FILE)
else:
    URL =  input("Please enter Youtube URL")
    convert_youTube(URL)


# STT인식 결과 
print('Model Start ' )
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
result = MODEL.transcribe(MP3_FILE)
print(result["text"])

print('Model END ' )
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print('Split Start ' )
splitAudio(result,MP3_FILE)
print('Split END ' )

## text : 인식결과 
## segments["id"] - 순서 
## segments["start"] - 시작시간 
## segments["end"] - 끝시간 

print("================= 파일 만들기 시작====================")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
with open(f"{MP3_FILE.split('.')[0]}.txt", "w", encoding="utf-8") as f:
    for r in result['segments']:
        f.write(f'[{r["start"]:.2f} --> {r["end"]:.2f}] {r["text"]}\n')
print("================= 파일 만들기 종료====================")
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 임시 WAV 파일 삭제 1
if(os.path.isfile(WAV_FILE)):
    os.remove(WAV_FILE)
    os.remove(amplified_wav_filename)
    print(f"{MP3_FILE} 및 {amplified_wav_filename} 파일이 삭제되었습니다.")

else:
    print("삭제할 임시 파일이 없습니다. 프로그램을 종료합니다.")