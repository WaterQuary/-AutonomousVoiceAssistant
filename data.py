import os
import webbrowser
import pyautogui
import random
import g4f
from g4f.Provider import Copilot
from datetime import datetime
import locale
import subprocess
import shutil


keyword = 'найди'
keyword_folder = 'названием'
keyword_time = 'время'
keyword_open = 'открой'

apps = {
    "калькулятор": "calc.exe",
    "блокнот": "notepad.exe",
    "проводник": "explorer.exe",
    "vs code": "code.exe",
    "командная строка": "cmd.exe"
}

def OpenApps(command):
    command = command.lower()
    ans = command.split()
    index = ans.index(keyword_open)
    ans = ans[index+1:]
    result = " ".join(ans)
    if result in apps:
        try:
            subprocess.Popen(apps[result])
            return f"Успешно открыла {result}"
        except FileNotFoundError:
            return "Ой, этот файл я не нашла, извиняюсь если затупила"
    else:
        exe_path = shutil.which(result)
        if exe_path != None:
            subprocess.Popen(exe_path)
            return f"Успешно открыла {result}"
        else:
            return "Ой, этот файл я не нашла, извиняюсь если затупила"
def Search(command):
    command = command.lower()
    ans = command.split()
    index = ans.index(keyword)
    ans = ans[index+1:]
    result = " ".join(ans)
    webbrowser.open(f'https://www.google.com/search?q={result}&hl=ru', new=2)
    return "Выполнено"
def next_track():
    pyautogui.press('nexttrack')
    return "Следующий трек"
def play_pause():
    pyautogui.press('playpause')
    return "Воспроизведение приостановлено"
def volume_up():
    pyautogui.press('volumeup', presses=5)
    return "Громкость увеличена"
def show_time():
        
        t = datetime.now().time().hour
        mins = datetime.now().time().minute
        ending = ''
        if t >= 2 and t <= 5 or t >= 22 and t <= 24:
            ending = 'часа'
        elif t == 1 or t == 21:
            ending = 'час'
        else:
            ending = 'часов'    

        if t >= 4 and t <= 11:
            time_resultt = (f"Сейчас {t} {ending} {mins} минут, утро")

        elif t >= 12 and t <= 16:
            time_resultt = (f"Сейчас {t} {ending} {mins} минут, день")

        elif t >= 17 and t < 22:
            time_resultt = (f"Сейчас {t} {ending} {mins} минут, вечер")

        else:
            time_resultt = (f"Сейчас {t} {ending} {mins} минут, ночь")
        
        time_resultt = str(time_resultt)

        print(time_resultt)
        return time_resultt
def AI(command):
    response = g4f.ChatCompletion.create(
            model="gpt-4",
            provider=Copilot,
            messages=[
                    {"role": "user", "content": "Ты голосовой помощник по имени Квари. Отвечай коротко, старайся избегать какого то кода или математических формул, только определения и слова." + command}
        ]
    )
    response = str(response)
    print(response)
    return response
def Create_folder(command):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if keyword_folder in command.lower():
        ans = command.split()
        index = ans.index(keyword_folder)
        ans = ans[index+1:]
        result = " ".join(ans)

        if not result:
            result = now

        path = os.path.join(desktop, result)

        if os.path.exists(path):
            path = os.path.join(desktop, now)
            os.makedirs(path, exist_ok=True)
            return(f"Папка уже существует, поэтому создаю папку на рабочем столе с другим названием: {now}")
        else:
            os.makedirs(path, exist_ok=True)
            return(f"Cоздаю папку на рабочем столе с названием: {result}")
    else:
        path = os.path.join(desktop, now)
        os.makedirs(path, exist_ok=True)
        return(f"Cоздаю папку на рабочем столе с названием: {now}")
def volume_down():
    pyautogui.press('volumedown', presses=5)
    return "Громкость уменьшена"
def what_date_now():
    now = datetime.now()
    locale.setlocale(locale.LC_TIME, 'rus')
    result = now.strftime("Сейчас: %d %B %Y")
    print(result) 
    return result
def Random_phrase(phrase):
    random.shuffle(phrase)
    result = phrase[0]
    return result

name = "Артём"

greetings_morning = [f"Доброе утро {name}. Как спалось? Хотя... не отвечайте, я и так знаю что отлично.",
                     f"{name}, доброе утро! Чего так рано? Но так даже лучше",
                     f"Наидобрейшего утра {name}. Что будем делать? А... я даже знаю, вы будете делать что-то полезное? угадала? конечно угадала, как иначе-то",
                     f"Доброе утро, {name}. Как дела? Хотяя... не отвечайте, я и так знаю что лучше всех",
                     f"{name}, доброе утро! Никогда не рано начать работать и развиваться",
                     f"{name}, а вы знаете пословицу. Кто рано встает тому бог подает? Так это про вас, развивайтесь пока все спят."]

greetings_afternoon = [f"Добрый день {name}. Как дела?",
                       f"День добрый {name}. Как погодка?",
                       f"{name} добрый день. Что хотите делать?"]

greetings_evening = [  f"{name} Добрый вечер. Как дела? Да ладно вам, можете не отвечать, я и так знаю что хорошо",
                       f"{name} добрый вечер. Устали от этого дня, но все равно сели работать? Уважаю. Помогу чем смогу",
                       f"Вечер добрый {name}. Никогда не поздно начать работать"]

greetings_night = [f"{name}, чего так поздно? Не спится? Но я все же думаю, что на вас накатила ночная мотивация. Работайте пока она есть",
                   f"Какие люди в такое время, {name}, я думаю сейчас не лучшее время чтобы работать и учиться. Но вы работайте и учитесь, это всегда полезно",
                   f"{name}, вы так поздно, может расслабитесь? Хотя, если хотите развиваться, я вам не мешаю",
                   f"Утро вечера мудреннее, {name}, но если вы считаете иначе то я не спорю.",
                   f"{name}, а не думали, почему ночью думается лучше? Ответ прост: ночью снижается уровень кортизола... это (гормон стресса), повышается активность подсознания, также активируется сенсорная депривация... это (отсутствие внешних раздражителей по типу шума или света). Все эти факторы и способствуют лучшему мышлению ночью. Так что... работайте и развивайтесь пока вы в таком режиме"]

shutdown = 'выключаю'            

gs2 = ['жду ваших указаний', 
       'Я вас слушаю', 
       'слушаю', 
       'принялА', 
       'возвращаюсь в режим ожидания', 
       'выключаюсь', 'Приятного Вечера!', 
       'Выполнено!',]

phrases = {
    "pause": 'пауза',
    "next_track": 'следующий трек',
    "volume_up": 'громче',
    "volume_down": 'тише',
    "data": 'дата',
    "time": 'время',
    "search": 'найди',
    "create_folder": 'папку',
    "openapps": "открой"
}

funcs = {
    "pause": play_pause,
    "next_track": next_track,
    "volume_up": volume_up,
    "volume_down": volume_down,
    "data": what_date_now,
    "time": show_time,
    "search": Search,
    "create_folder": Create_folder,
    "openapps": OpenApps
}
