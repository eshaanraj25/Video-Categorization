# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 18:40:58 2021

@author: Sai Ji
"""
import sys
import os
import classify_nsfw_video
import classify_nsfw
import AudioExtractor
from multiprocessing import Process
import Controller

nsfw_score=0
nsfw=False
audio_score=0
data=''
category=''
def func1(src):
     global nsfw_score
     global nsfw
     print("function1 called")
     #import subprocess
     #s_out=subprocess.check_output([sys.executable,"classify_nsfw_video.py"," -m D:/Degree/7th Sem/Minor project/Video Categorisation/data/open_nsfw-weights.npy ", path])
     #print("SOUT:: "+s_out)
     os.system("python classify_nsfw_video.py -m data/open_nsfw-weights.npy D:/Degree/7thSem/Minorproject/VideoCategorisation/videos/"+src +" >> result.txt")
     infile = open('D:/Degree/7thSem/Minorproject/VideoCategorisation/result.txt', 'r')
     firstLine = infile.readline()
     print("FIRST LINE::",firstLine.strip())
     if(firstLine.strip() =="NSFW"):
         nsfw=True
         print("NSFW IN IF STATEMENT: ",nsfw)
         nsfw_score=float(infile.readline())
         print("NSFW SCORE: ",nsfw_score)
     infile.close()    
     os.remove("D:/Degree/7thSem/Minorproject/VideoCategorisation/result.txt")

def func2(folder,file):
    global audio_score
    audio_score=AudioExtractor.main(folder,file)

def main(folder,src):
    #path=folder+src
    func1(src)
    func2(folder,src)
    print("IS NSFW:? ",nsfw)
    print("NSFW SCORE: ",nsfw_score)
    print("AUDIO SCORE: ",audio_score)
    global data
    global category
    if(nsfw):
        #if(audio_score["abusive"] and audio_score["hate_speech"]):
        if(nsfw_score>40):
            data = [{"NSFW" : True, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
            category ='18+'
            return "/final"
        elif(nsfw_score>20 and nsfw_score<40):
            if((audio_score["abusive"]>0.6 and audio_score["abusive"]<1.0) or (audio_score["hate_speech"]>0.7 and audio_score["hate_speech"]<1.0)):
                data = [{"NSFW" : True, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
                category ='18+'
                return "/final"
            elif((audio_score["abusive"]>0.3 and audio_score["abusive"]<0.6) or (audio_score["hate_speech"]>0.4 and audio_score["hate_speech"]<0.7)):
                data = [{"NSFW" : True, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
                category ='13+'
                return "/final"
        else:
            if((audio_score["abusive"]>0.6 and audio_score["abusive"]<1.0) or (audio_score["hate_speech"]>0.7 and audio_score["hate_speech"]<1.0)):
                data = [{"NSFW" : False, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
                category ='13+'
                return "/final"
            elif((audio_score["abusive"]>0.3 and audio_score["abusive"]<0.6) or (audio_score["hate_speech"]>0.4 and audio_score["hate_speech"]<0.7)):
                data = [{"NSFW" : False, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
                category ='7+'
                return "/final"  
            else:
                data = [{"NSFW" : False, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
                category ='3+'
                return "/final"
    elif(not nsfw):
        if((audio_score["abusive"]>0.6 and audio_score["abusive"]<1.0) or (audio_score["hate_speech"]>0.7 and audio_score["hate_speech"]<1.0)):
            data = [{"NSFW" : True, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
            category ='15+'
            return "/final"
        elif((audio_score["abusive"]>0.3 and audio_score["abusive"]<0.6) or (audio_score["hate_speech"]>0.4 and audio_score["hate_speech"]<0.7)):
            data = [{"NSFW" : False, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
            category ='7+'
            return "/final"
        else:
            data = [{"NSFW" : False, "nsfw_score" : nsfw_score, "audio_score" : audio_score}]
            category ='3+'
            return "/final"
   
    return "/final"
    
def getdata():
    print("DATA: ",data)
    return data

def getCategory():
    print("CATEGORY: ",category)
    return category
    
if __name__=='__main__':
     main(sys.argv)