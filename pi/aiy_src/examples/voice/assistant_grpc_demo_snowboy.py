#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import argparse
import locale
import logging
import signal
import sys
sys.path.append('/home/pi/snowboy/examples/Python3')

models = ['/home/pi/Downloads/hi_bidi.pmdl',
          '/home/pi/Downloads/bidi.pmdl']

from aiy.assistant.grpc import AssistantServiceClientWithLed
from aiy.board import Board

import mod.snowboydecoder as snowboydecoder

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant with customised hotword')
    parser.add_argument('--language', default=locale_language())
    parser.add_argument('--volume', type=volume, default=60)
    parser.add_argument('--model', default='/home/pi/Downloads/hi_bidi.pmdl')
    args = parser.parse_args()

    detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)
    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,
                                                  volume_percentage=args.volume,
                                                  language_code=args.language)
        while True:
            logging.info('say hi bidi to start conversation ...')
            detector.start()
            logging.info('Conversation started!')
            assistant.conversation()

if __name__ == '__main__':
    main()
