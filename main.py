import json
import pyaudio
from speakerpy.lib_speak import Speaker
from vosk import KaldiRecognizer, Model
from datetime import datetime
import data

class VoiceAssistant:

  def __init__(self):
    self.model = Model(
        r'C:\Users\User\Desktop\secret\ZhestkoVosk\vosk-model-small-ru-0.22'
    )
    self.recognizer = KaldiRecognizer(self.model, 16000)
    self.trigger_words = [
        'аквариум',
        'к фары',
        'кварты',
        'квар и',
        'гвардии',
        'кларе',
        'твари',
        'квари',
        'клары',
        "к вары",
        "к клары"
    ]
    self.dictionary = data.phrases
    self.speaker = Speaker(
        model_id='ru_v3', language='ru', speaker='baya', device='cpu'
    )
    self.funcs = data.funcs
    self.keyword = data.keyword
    self.mic = pyaudio.PyAudio()
    self.time = int(datetime.now().time().hour)
    self.stream = self.mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    self.stream.start_stream()
    self.commands = { 
       data.shutdown: self.close,
    }
    for key, value in self.dictionary.items():
        if key in self.funcs:
            self.commands[value] = self.funcs[key]
    
  def speak(self, text, speed=1.0, sample_rate=48000):
    self.speaker.speak(text=text, sample_rate=sample_rate, speed=speed)

  def get_text(self):
    res = json.loads(self.recognizer.Result())
    return res.get('text', '').strip()

  def run(self):
    try:
      if self.time >= 4 and self.time <= 11:
          self.speak(data.Random_phrase(data.greetings_morning))
      elif self.time >= 12 and self.time <= 16:
          self.speak(data.Random_phrase(data.greetings_afternoon))
      elif self.time >= 17 and self.time < 22:
          self.speak(data.Random_phrase(data.greetings_evening))
      else:
          self.speak(data.Random_phrase(data.greetings_night))
      while True:
        self.status_waiting()
    except KeyboardInterrupt:
      self.close()

  def status_waiting(self):
    print('СТАРТ')
    while True:
      audio_bytes = self.stream.read(8192, exception_on_overflow=False)
      if self.recognizer.AcceptWaveform(audio_bytes):
        finally_text = self.get_text()
        if not finally_text:
          continue

        print(finally_text)

        if finally_text.lower() in self.trigger_words:
          self.speak('Слушаю')
          print('ПЕРЕХОД')
          self.status_listen()
          print('СТАРТ')
        elif finally_text.lower() == 'пока':
          print('Прощай')
          self.speak('Прощай')
          self.close()
          exit(0)

  def status_listen(self):
    print('СЛУШАЮ')
    while True:
      audio_bytes = self.stream.read(8192, exception_on_overflow=False)
      if self.recognizer.AcceptWaveform(audio_bytes):
          finally_text = self.get_text()
          if not finally_text:
            continue

          if finally_text.lower() == 'прощай':
            print('Выход из режима прослушивания')
            return
          
          command = finally_text.lower().strip()
          
          command_found = False
          print(command)
          for phrase, func in self.commands.items():
            if phrase in command:
              try:
                self.speak(func(command))
              except TypeError:
                self.speak(func())    
              command_found = True
              return 
            
          if not command_found:
              self.speak("НЕ ПОНЯЛА КОМАНДЫ, ВОЗВРАЩАЮСЬ")
              # self.speak(data.AI(command))
              return

  def close(self):
    self.stream.stop_stream()
    self.stream.close()
    self.mic.terminate()


if __name__ == '__main__':
  assistant = VoiceAssistant()
  assistant.run()
