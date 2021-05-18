import locale
import logging
import signal
import datetime
import numpy as np
from intents import *
from aiy.voice import tts
from aiy.cloudspeech import CloudSpeechClient

import sys
sys.path.append('/home/pi/snowboy/examples/Python3')
import mod.snowboydecoder as snowboydecoder

LANG, _ = locale.getdefaultlocale()
HOTWORDS = ['/home/pi/src/pi/hot_words/hi_bidi.pmdl',
            '/home/pi/src/pi/hot_words/bidi.pmdl']

def speak(text, **kwargs):
    tts.say(text, **kwargs)
    
def get_hints(language_code):
    if language_code.startswith('en_'):
        return hints
    return None

def action_nav(intent):
    action_nav_dict = {i: speak for i in intents_dict}
    return action_nav_dict[intent]

def text_nevigator(text):
    text = text.lower()
    print('bidi heard:', text)
    answered = False
    for intent, phrases in intents_dict.items():
        if text in phrases:
            if intent == 'time':
                action_nav(intent)(get_time)
            else:
                action_nav(intent)(np.random.choice(replies[intent]))
            answered = True
            break
    if not answered:
        speak('not sure what is: '+text, volume=40)
          
    if answered and intent == 'exit':
        return 'exit now'
    return text

def get_time():
    return datetime.datetime.today().strftime('%a, %x %X')


    
def listen():
    speak('bidi, at your service', volume=30,)
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    detector = snowboydecoder.HotwordDetector(HOTWORDS, sensitivity=0.5)

    client = CloudSpeechClient()
    
    listen = 1
    while(listen):
        logging.info('say hi bidi to start conversation ...')
        detector.start()
        logging.info('talk to bidi, dont be shy...')

        print('now listening')
        text = client.recognize(language_code=LANG,
                                hint_phrases=get_hints(LANG))
        
        if text:
            print(text)
            text = text_nevigator(text)
            if text == 'exit now':
                print('breaking listening loop. bye bye')
                listen = 0