import subprocess
import datetime
from threading import Timer,Thread,Event

PROCESS_NAME = ['python3', '-u', 'keyBot.py']

bot = ''

class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

def looper():
    global bot
    if check_input(bot.poll(), 1):
        print(str(datetime.datetime.now())+" restart! ")
        print(str(bot.communicate())+'\n')
        bot = create_child_gen(PROCESS_NAME)


def create_child_gen(run):
    ret = -1
    try:
        ret = subprocess.Popen(run, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except ChildProcessError:
        print('Subprocess generation error')
    return ret


def check_input(expected, received):
    return isinstance(received, type(expected))

def main():
    global bot
    bot = create_child_gen(PROCESS_NAME)
    tim = perpetualTimer(3600, looper)
    tim.start()

main()
