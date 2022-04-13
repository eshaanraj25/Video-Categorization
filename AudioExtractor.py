# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:35:12 2021

@author: Sai Ji
"""

import moviepy.editor as mp
#my_clip = mp.VideoFileClip(r"C:\Users\Sai Ji\Downloads\tensorflow-open_nsfw-master 2\22.mp4")
#my_clip.audio.write_audiofile(r"my_result.wav")


"""
Next Task is to compress .wav file
or find speech recoganition for large files.
(google speech is option but PAID)
"""
import sys
import paralleldots
import speech_recognition as sr 
import os
from SplitWavAudioMubin import SplitWavAudioMubin
import shutil

# create a speech recognition object
r = sr.Recognizer()
api_key   = "cu7WLtAD14PXShAdUN0XN7kkciALa4MWJlnMNeAoTeU"
paralleldots.set_api_key( api_key )

def main(folder,file):
    AudioFromVideo(folder,folder+file)
    split_wav = SplitWavAudioMubin(folder, "AudioExtracted.wav")
    split_wav.multiple_split(min_per_split=1)
    abuse=get_large_audio_transcription(folder+"audio-chunks/")
    folder_path = folder+"audio-chunks"
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)
    return abuse

def AudioFromVideo(folder,path):
    print("AUDIO VIDEO: PATH: ",path)
    my_clip = mp.VideoFileClip(path)
    my_clip.audio.write_audiofile(folder+"AudioExtracted.wav")

# a function that splits the audio file into chunks
# and applies speech recognition

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    
    allfiles= os.listdir(path)
    print("SRC: ",allfiles)
    whole_text = ""
    # process each chunk 
    for entry in allfiles:
        # recognize the chunk
        with sr.AudioFile(path+entry) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(entry, ":", text)
                whole_text += text
    # return the text for all chunks detected
    abuse= paralleldots.abuse( whole_text )
    print(abuse)
    return abuse

if __name__ == '__main__':
    #user will insert a valid video path to this function
    #whole_text=get_large_audio_transcription(r"C:\Users\Sai Ji\Downloads\tensorflow-open_nsfw-master 2\my_result.wav")
    #print("WHOLE TEXT= ",whole_text)
    main(sys.argv)