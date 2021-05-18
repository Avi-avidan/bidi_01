

intents_dict = {}
intents_dict['turn_lights_on_hw'] = ['lights on', 'turn on the light', 'turn lights on']
intents_dict['turn_lights_off_hw'] = ['lights off', 'lights out', 'turn off the light', 'turn lights off']
intents_dict['say_ip_hw'] = ["what's your ip", 'ip address', 'ip', "what's your ip address"]
intents_dict['positive_feedback'] = ["that's great", 'cool', 'thank you', "that's nice", 'wow']
intents_dict['lidar_hw'] = ['look around', 'explore', 'lidar on', 'blink']
intents_dict['time'] = ['what time is it', 'time is it', 'time', 'do you have the time', 'can you tell me wahat time is it']
intents_dict['exit'] = ['exit', 'shutdown', 'stop listening', 'enough', "that's it for now"]

replies = dict()
replies['turn_lights_on_hw'] = ['turning lights on']
replies['turn_lights_off_hw'] = ['lights off']
replies['say_ip_hw'] = ['']
replies['positive_feedback'] = ['no problem', 'no sweat', "don't mention it", 'you got it', 'your wish is my command']
replies['lidar_hw'] = ['scanning']
intents_dict['time'] = ['']
replies['exit'] = ['bye bye']



hints = [p for v in intents_dict.values() for p in v]