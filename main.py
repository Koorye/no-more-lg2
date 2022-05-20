import json
import os
from os import system, name

from user import User

def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def print_green(s, end='\n'):
    print('\033[32m' + s + '\033[0m', end=end)

def print_red(s, end='\n'):
    print('\033[31m' + s + '\033[0m', end=end)

class Client(object):
    def __init__(self, prop_path='prop.json'):
        if not os.path.exists(prop_path):
            self.input_prop()    
        else:
            self.read_prop(prop_path)
        
        clear_screen()
        self.user = User(self.username, self.password)
        self.user.login()

        self.handle_op()
    
    def input_prop(self):
        username = input('请输入用户名：')
        password = input('请输入密码：')
        self.username = username
        self.password = password
    
    def read_prop(self, prop_path):
        with open(prop_path) as f:
            res = json.load(f)
        self.username = res['username']
        self.password = res['password']
    
    def save_prop(self, prop_path='prop.json'):
        with open(prop_path, 'w') as f:
            json.dump(dict(
                username=self.username,
                password=self.password,
            ), f)
    
    def handle_op(self):
        msg, log = None, 'info'
        while True:
            clear_screen()
            print(self.user.show_info())
            if msg is not None:
                print('-'*60) 
                if log == 'success':
                    print_green(str(msg))
                elif log == 'error':
                    print_red(str(msg))
                else:
                    print(msg)
            
            print('-'*60) 
            print('1. 查看活动')
            print('2. 报名活动')
            print('3. 签到活动')
            print('4. 查看课程')
            print('5. 签到课程')
            print('6. 循环签到课程')
            print('q. 退出')
            print('-'*60) 
            res = input('请输入操作序号：').strip()

            try:
                if res == '1':
                    self.user.get_activities()
                    msg = self.user.show_activities()
                    log = 'info'
                elif res == '2':
                    idx = int(input('请输入活动序号：').strip())
                    msg = self.user.register(idx)
                    log = 'success'
                elif res == '3':
                    idx = int(input('请输入活动序号：').strip())
                    msg = self.user.sign(idx)
                    log = 'success'
                elif res == '4':
                    self.user.get_courses()
                    msg = self.user.show_courses()
                    log = 'info'
                elif res == '5':
                    idx = int(input('请输入课程序号：').strip())
                    msg = self.user.sign_course(idx)
                    log = 'success'
                elif res == '6':
                    idx = int(input('请输入课程序号：').strip())
                    msg = self.user.loop_sign_course(idx)
                    log = 'success'
                elif res == 'q':
                    self.save_prop()
                    exit(0)
            except Exception as e:
                msg = e
                log = 'error'


if __name__ == '__main__':
    client = Client()