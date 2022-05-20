import pandas as pd
import time

from api import Api


pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

class User(object):
    def __init__(self, username, password):        
        self.username = username
        self.password = password
        self.header = dict()

        self.activities = None
        self.courses = None

        self.id_ = None
        self.org = None
        self.school = None
        self.nickname = None
        self.phone = None
        self.week_index = None

        self.api = Api()
    
    def login(self):
        res = self.api.req('login', data={
            'userName': self.username,
            'password': self.password,
        })
        
        self.id_ = res['id']
        self.org = res['organizationName']
        self.school = res['schoolName']
        self.nickname = res['nickName']
        self.phone = res['mobile']

        self.header['authorization'] = 'Bearer ' + res['accessToken']
        self.header['Organization'] = res['schoolId']
        
        res = self.api.req('current', header=self.header)
        self.week_index = res['weekIndex']
    
    def get_activities(self):
        def get_status(activity):
            is_register = activity['isRegister']
            is_sign = activity['signTime'] is not None
            sign_time = activity['signTime']
            if not is_register:
                return '未报名'
            elif not is_sign:
                return '未签到'
            elif sign_time == 1:
                return '已签到一次'
            elif sign_time == 2:
                return '已签到完成'
        
        def get_interval(activity):
            if activity['signTime'] is None:
                return '-'
            interval = self.api.req('interval', data={
                'activityId': activity['id']
            }, header=self.header)['timeInterval']
            if interval is None:
                return '-'
            interval = int(interval) // 1000
            minute = interval // 60
            second = interval % 60
            return f'{minute}:{second}'
        
        res = self.api.req('activity', header=self.header)['items']

        if res is not None:
            for res_ in res:
                res_['status'] = get_status(res_)
                res_['interval'] = get_interval(res_)
            
        self.activities = res

    def register(self, idx):
        activity_id = self.activities[idx]['id']
        res = self.api.req('register', data={
            'activityId': activity_id,
        }, header=self.header)
        if res['success'] == False:
            raise Exception(res['reason'])
        return res

    def sign(self, idx):
        activity_id = self.activities[idx]['id']
        res = self.api.req('sign', data={
            'userId': self.id_,
            'activityId': activity_id,
        }, header=self.header)
        return res
    
    def get_courses(self):
        res = self.api.req('course', header=self.header)
        self.courses = res
     
    def sign_course(self, idx):
        course_id = self.courses[idx]['id']
        res = self.api.req('signCourse', data={
            'userId': self.id_,
            'weekNumber': self.week_index,
            'courseId': course_id,
            }, header=self.header)
        return res
            
    
    def loop_sign_course(self, idx, loop_every=30.):
        course_id = self.courses[idx]['id']
        idx = 1
        while True:
            print(f'第{idx}次尝试: ', end='')
            try:
                res = self.api.req('signCourse', data={
                        'userId': self.id_,
                        'weekNumber': self.week_index,
                        'courseId': course_id,
                        }, header=self.header)
                print(res)
            except Exception as e:
                if '已签到' in str(e):
                    raise e
            idx += 1
            time.sleep(loop_every)         
   
    def show_courses(self, col_include=['name', 'weekLabel', 'courseStatusStr']):
        df = pd.DataFrame(self.courses)
        df['name'] = df['name'].apply(lambda x: x[:20] + '...' if len(x)>20 else x)
        df = df[col_include]
        return df.transpose()

    def show_activities(self, col_include=['name', 'stateName', 'status', 'interval']):
        df = pd.DataFrame(self.activities)
        df = df[col_include]
        return df
    
    def show_info(self):
        df = pd.DataFrame({
            'nickname': [self.nickname],
            'school': self.school,
            'organization': self.org,
            'phone': self.phone,
        })
        return df.transpose()
