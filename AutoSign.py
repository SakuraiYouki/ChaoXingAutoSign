import requests
from requests.sessions import session
from lxml import etree
import base64
import re
from itertools import combinations

global currClass
currClass=0
def login(username,password):
    url='http://passport2.chaoxing.com/fanyalogin'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Referer': r'http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com'
    }
    
    data={
        'fid':-1,
        'uname':username,
        'password':base64.b64encode(password.encode()).decode(),
        'refer':r'http%253A%252F%252Fi.chaoxing.com',
        't':True,
        'forbidotherlogin':0
    }
    global session
    session=requests.session()
    res=session.post(url,headers=headers,data=data)
    #print(res.cookies)

def getclass():

    url='http://mooc1-2.chaoxing.com/visit/courses'

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Referer': r'http://i.chaoxing.com/'

    }
    res=session.get(url,headers=headers)
    #print(res.text)

    if res.status_code==200:
            class_HTML=etree.HTML(res.text)
            #print("处理成功，您当前已开启的课程如下：")
            i=0
            global course_dict
            course_dict={}

            for class_item in class_HTML.xpath("/html/body/div/div[2]/div[3]/ul/li[@class='courseItem curFile']"):
                #courseid=class_item.xpath("./input[@name='courseId']/@value")[0]
                #classid=class_item.xpath("./input[@name='classId']/@value")[0]
                try:              
                    class_item_name=class_item.xpath("./div[2]/h3/a/@title")[0]
                
                    #等待开课的课程由于尚未对应链接，所有缺少a标签。
                    i+=1
                    #print(class_item_name)
                    course_dict[i]=[class_item_name,"https://mooc1-2.chaoxing.com{}".format(class_item.xpath("./div[1]/a[1]/@href")[0])]
                except:
                    pass
            #print("———————————————————————————————————")
    else:
            print("error:课程处理失败")

def qiandao(url:str,address:str,enc:str):
   
    url='https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId={courseid}&jclassId={clazzid}'.format(courseid=re.findall(r"courseid=(.*?)&",url)[0],clazzid=re.findall(r"clazzid=(.*?)&",url)[0])
    #print(url)
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    }
    res=session.get(url,headers=headers)
    #print(res.text)
    tree=etree.HTML(res.text)
    #fid=tree.xpath('/html/body/input[4]/@value')
    activeDetail=tree.xpath('/html/body/div[2]/div[2]/div/div/div/@onclick')
    if not activeDetail:
        print(course_dict[currClass][0]+"------暂无签到活动")
    else:
        print('\n')
        print(course_dict[currClass][0]+"------检测到："+str(len(activeDetail))+"个活动。")
        for activeID in activeDetail:
            global id
            id=re.findall(r'activeDetail\((.*?),',activeID)
            url='https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId={id}&clientip=&latitude=-1&longitude=-1&appType=15&fid=0&enc={enc}&address={address}'.format(id=id[0],enc=enc,address=address)
            #print(url)
            res=session.get(url,headers=headers)
            #url='https://mobilelearn.chaoxing.com//widget/sign/pcStuSignController/checkSignCode?activeId={id}&signCode={signcode}'.format(id=id[0],signcode=1236)
            #res=session.get(url,headers=headers)
            #print(url)
            print('**********')
            print(res.text)
        print('\n')
            



if __name__=='__main__':
    username=input('请输入账号：')
    password=input('请输入密码：')
    
    address=input('请输入位置签到所需位置（没有请忽略）：')
    enc=input('请输入二维码签到的ENC（没有请忽略）')
    login(username,password)
    getclass()

    #print(course_dict)
    for currClass in course_dict:
        #print(course_dict[i][1])
        qiandao(course_dict[currClass][1],address,enc)

    
    #gen_password()
    #print(course_dict)