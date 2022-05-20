import json
import requests


base_url = 'https://cpes.legym.cn/'

api = dict(
    # 登录
    login=dict(
        url='authorization/user/manage/login',
        method='post',
        data=dict(
            entrance=1,
            username=None,
            password=None)),
    # 获取当前信息
    current=dict(
        url='education/semester/getCurrent',
        method='get',
        data=None,
    ),
    # 获取活动列表
    activity=dict(
        url='education/app/activity/getActivityList',
        method='post',
        data=dict(
            page=1,
            size=100)),
    # 获取活动签到剩余时间
    interval=dict(
        url='education/app/activity/checkSignInterval',
        method='get',
        data=dict(activityId=None)),
    # 报名活动
    register=dict(
        url='education/app/activity/signUp',
        method='post',
        data=dict(activityId=None)),
    # 签到活动
    sign=dict(
        url='education/activity/app/attainability/sign',
        method='put',
        data=dict(
            times='1',
            pageType='activity',
            activityType=0,
            attainabilityType=1,
            userId=None,
            activityId=None)),
    # 获取课程列表
    course=dict(
        url='education/course/app/forStudent/list',
        method='get',
        data=None,
    ),
    # 课程签到
    signCourse=dict(
        url='education/course/app/forStudent/sign',
        method='put',
        data=dict(
            attainabilityType='0',
            pageType='course',
            startSignNumber=1,
            weekNumber=None,
            courseId=None,
            userId=None)),
)

class Api(object):
    def __init__(self):
        self.base_url = base_url
        self.api = api
        self.header = {"content-type": "application/json"}
    
    def req(self, type_, data=None, header=None):
        api = self.api[type_]
        method = api['method']

        original_data = api['data']
        if data is not None and original_data is not None:
            for key in data:
                original_data[key] = data[key]
        data = original_data

        original_header = self.header.copy()
        if header is not None and original_header is not None:
            for key in header:
                original_header[key] = header[key]
        header = original_header

        if method == 'get':
            res = requests.get(base_url + api['url'], params=data, headers=header)
        elif method == 'post':
            res = requests.post(base_url + api['url'], json=data, headers=header)
        elif method == 'put':
            res = requests.put(base_url + api['url'], json=data, headers=header)
        else:
            raise NotImplementedError()
        
        if res.status_code == 200:
            return json.loads(res.text)['data']
        else:
            raise Exception(json.loads(res.text)['message'])
        