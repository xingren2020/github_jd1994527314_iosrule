# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : TG Bot
   Author   : 红鲤鱼与绿鲤鱼与驴
   date     : 2021-2-2 21:32 
   Desc     : 公众号iosrule,编程测试与学习
   Gamerule: Tg群，微信学习，请勿用于非法用途
   update: 1:2021.2.4 修复管理员删除字符bug,修复下超时重置清0.2.修复超时逻辑判断，添加改版前上车人数据代码。调整活动简称。2:2.5加入权限3:2.6修改漏写注册圈友数据4.2.8增加稳定数据算法5.2.10群友反应很多人不跑互助码库，只能增加群友要求功能:群友要求可以定期清空数据，清理不助力的群友互助码。
-------------------------------------------------
"""

import requests
import json
import time
import timeit
import os
import re
import random
import urllib
from datetime import datetime
from dateutil import tz


tg_bot_id=''
tg_member_id=''
tg_group_id=''
tg_new_id=''
tg_bot_cmd=''
tg_admin_id=''
tg_ac_id=''
longid=0
upid=0
hd_int_mem=0
hd_int_code=[]


#远程配置
heartnum=120
r=2


ac_database=''
osenviron={}
telelist=[]
result=''
hd_memjson={}
reset=1
reboot=1
#=====================================



#=====================================
command=['/function','/submit','/view','/zhuce','/admin_viewallid','/admin_addid','/admin_delid','/admin_delcode','/admin_viewcode','/admin_reboot','/admin_reset']
description=['功能简介:','提交功能','查询上车和我的提交互助码','注册上车权限限','管理员查看所有id','管理员处理审核加入id','管理员处理投诉后删除ID','管理员删除错误互助码','管理员查询互助码','管理员重启机器人','管理员清空所有数据']
hd_nm=['NC@京东农场','NS@年兽','MC@萌宠','JC@惊喜工厂','DC@京东工厂','ZD@种豆','MH@盲盒','JN@京喜农场']
hd_me=['ME@注册圈友人数']
bot_zhuce=['请注册后使用','你好,很多群友反应加了互助码库，却没有跑互助码库脚本，只有他们给你助力，你却没有给他们助力，所以采用微信群友审核机制，他们审核同意后，联系公众号iosrule,群主加入权限.本人只提供机器人服务，其他不懂','你已经上车','你好，群友偶尔如有要求助力截图,请在群里发助力截图']
hd_codelist=[]
hd_memlist=[]
zhjbzhenda=[]
bot_timeout=15
bot_fix=0
fixtime=15

tback=['1.机器响应时间15-30秒,请在对话框输入字符 /  查看对应指令再发送内容。每个京东活动互助码分开提交,格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556\n',]
#=====================================
def help_update():
   help=''
   try:
      help+='2.当前互助码活动(动态更新中):'+str(hd_nm)+'\n'
      return help
   except Exception as e:
      pass


      
      
def bot_load():
   global hd_codelist,hd_int_mem,hd_memjson,hd_int_code
   try:
      for ll in hd_nm:
        tmp=bot_rd(ll[0:2],ll[3:len(ll)])
        hd_codelist.append(tmp)
        hd_int_code.append(len(tmp))
      hd_memjson=bot_rd(hd_me[0][0:2],hd_me[0][3:len(hd_me[0])])
      hd_int_mem=len(hd_memjson)

      ac_data()
   except Exception as e:
      msg=str(e)
      print('bot_load'+msg)
      
      
def ac_data():
   try:
      global ac_database
      print('\n成功上车人数')
      ac_database='1.【已上车人数】'+str(hd_int_mem)+'\n'
      for i in range(len(hd_int_code)):
        ac_database+='【'+hd_nm[i][3:len(hd_nm[i])]+'互助码数】'+str(hd_int_code[i])+'\n'
      print(ac_database)
   except Exception as e:
      msg=str(e)
      pass
def bot_update():
   global longid,upid,bot_fix
   try:
      longid+=1
      ufo=''
      m=8
      if longid>m:
        print('clean=======:::::=')
        print(len(tg_new_id))
        ufo=tg_new_id+str(upid)
        longid=0
      else:
      	ufo=tg_bot_id
      res=requests.get(ufo,timeout=200).json()
      if 'result' in res:
         upid=res["result"][len(res["result"])- 1]["update_id"]
      return res
   except Exception as e:
      msg=str(e)
      bot_fix=fixtime
      print('bot_update'+msg)
      bot_sendmsg(tg_admin_id,'机器人超时',msg)
      
      
def bot_loadmsg():
   try:
      res=bot_update()
      if not 'result' in res:
        print('退出')
        return 
      if len(res['result'])==0:
        print('退出')
        return 
      bot_primsg(res)
   except Exception as e:
      msg=str(e)
      print('bot_loadmsg'+msg)
def bot_primsg(res):
   try: 
     global msglist
     username=''
     msgtext=''
     msglist=[]
     i=0
     for data in res['result']:
        if data['message']['chat']['type']!='private':
           continue
        if 'username' in data['message']['chat']:
          username=data['message']['chat']['username']
        if 'first_name' in data['message']['chat']:
          username+='_'+data['message']['chat']['first_name']+'_'+data['message']['chat']['first_name']
        if 'last_name' in data['message']['chat']:
             username+='_'+data['message']['chat']['last_name']
        id=data['message']['chat']['id']
        if 'text' in data['message']:
             msgtext=data['message']['text']
        else:
          msgtext='no msg'
        smslist=[]
        cc=False
        for i in range(len(msglist)):
          if id in msglist[i]:
             msglist[i].append(msgtext)
             msglist[i].append(data['message']['date'])
             cc=True
        if cc==False:
           smslist.append(id)
           smslist.append(username)
           smslist.append(msgtext)
           smslist.append(data['message']['date'])
           msglist.append(smslist)
     print('约会人数:'+str(len(msglist)))
   except Exception as e:
      msg=str(e)
      print('bot_primsg'+msg)

      
def bot_sendmsg(id,title,txt):
   try:
      txt=urllib.parse.quote(txt)
      title=urllib.parse.quote(title)
      turl=f'''{tg_member_id}chat_id={id}&text={title}\n{txt}'''
      response = requests.get(turl)
      #print(response.text)
   except Exception as e:
      msg=str(e)
      print(id+'_bot_sendmsg_'+msg)
def bot_chat():
   try:
       global bot_fix
       postmsg=''
       stoploop=False
       #print(msglist)
       print('会话个数:',str(len(msglist)))
       if len(msglist)==0:
         return
       for i in range(len(msglist)):
          print(str(i+1)+'.=================')
          txttm=0
          checktm=0
          newmsglist=[]
          xo2=0
          xo1=0
          m1=0
          m2=0
          id=str(msglist[i][0])
          nm=msglist[i][1]
          if len(msglist[i])==0:
            continue
          if len(msglist[i])>4:
            mm1=msglist[i][len(msglist[i])-4]
            mm2=msglist[i][len(msglist[i])-2]
            xo2=msglist[i][len(msglist[i])-3]
            xo1=msglist[i][len(msglist[i])-1]
          elif len(msglist[i])==4:
            xo1=msglist[i][len(msglist[i])-1]
            mm2=msglist[i][len(msglist[i])-2]
          print('开始时间:'+datetime.fromtimestamp(msglist[i][3]).strftime('%Y-%m-%d %H:%M:%S'))
          print('结束时间:'+datetime.fromtimestamp(xo1).strftime('%Y-%m-%d %H:%M:%S'))
          checktm=int(tm10())-xo1
          checkmt=int(tm10())-xo2
          print('【会话+'+str(i+1)+'+】超时'+str(checktm)+'检验:'+str(bot_fix))
          print('【会话+'+str(i+1)+'+】超时'+str(checkmt)+'检验:'+str(bot_fix))
          
          if checktm>bot_timeout*2+3+bot_fix:
             print('机器人接收上个信息超时.....')
             bot_fix=0
             continue
          if len(msglist[i])>4:
             if checkmt<bot_timeout*2+5+bot_fix:
                 newmsglist.append(mm1.strip())
                 newmsglist.append(mm2.strip())
                 bot_checkwrong(id,nm,newmsglist,2)
                 bot_admin(id,newmsglist,2)
             else:
                 newmsglist.append(mm2.strip())
                 bot_checkwrong(id,nm,newmsglist,1)
                 bot_admin(id,newmsglist,1)
          elif len(msglist[i])==4:
            newmsglist.append(mm2.strip())
            bot_checkwrong(id,nm,newmsglist,1)
            bot_admin(id,newmsglist,1)
   except Exception as e:
      msg=str(e)
      print('bot_chat:'+msg)
      


def bot_checkwrong(id,nm,mlist,pop):
  try:
    postmsg=''
    print('通用数据验证====='+str(pop),mlist)
    if pop==1:
       if mlist[0]=='/function':
          if not me(id):
            return
          postmsg=tback[0]+help_update()
          bot_sendmsg(id,'机器人功能',postmsg)
       elif mlist[0]=='/view':
          if not me(id):
            return
          sendview(id)
          
       elif mlist[0]=='/zhuce':
               me(id,1)
    elif pop==2:
      if mlist[0] in command and mlist[1] in command:
        for i in range(2):
           if mlist[1]=='/function':
             if not me(id):
               return
             postmsg=tback[0]+help_update()
             bot_sendmsg(id,'帮助功能',postmsg)
           elif mlist[1]=='/view':
               if not me(id):
                  return
               sendview(id)
              
           elif mlist[i]=='/zhuce':
               me(id)
      elif mlist[0] in command and mlist[1] not in command:
        if mlist[0]=='/submit':
          i=0
          if not me(id):
            return
          for ll in hd_nm:
            i+=1
            print('check hd:'+ll[0:2])
            if mlist[1].find(ll[0:2])==0:
               print('add======')
               postmsg=mlist[1][2:len(mlist[1])]
               print('get code:'+postmsg)
               allnum=len(postmsg.strip().split('@'))
               for code in postmsg.strip().split('@'):
                 if len(code)<4:
                    allnum-=1
                    continue
                 if code in hd_codelist[i-1]:
                   print('数据库重复数据，跳过====')
                   allnum-=1
                   continue
                 hd_codelist[i-1].append(code)
                 _addcodeid(id,mlist[1][0:2]+code)
               postmsg=ll[3:len(ll)]+'活动共计提交'+str(len(postmsg.strip().split('@')))+'个互助码,其中'+str(allnum)+'个为有效互助码，其他为重复数据,1个小时后更新进数据库....'
               break
            else:
               postmsg=nm+'请勿发送无效互助码....格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556'
          bot_sendmsg(id,'提交功能',postmsg)
        elif mlist[0]=='/function':
             if not me(id):
               return
             postmsg=tback[0]+help_update()
             bot_sendmsg(id,'帮助功能',postmsg)
        elif mlist[0]=='/view':
               if not me(id):
                 return
               sendview(id)
      elif mlist[0] not in command and mlist[1] in command:
       if mlist[1]=='/function':
          if not me(id):
            return
          postmsg=+help_update()
          bot_sendmsg(id,'查询功能',postmsg)
       elif mlist[1]=='/view':
          if not me(id):
            return
          sendview(id)
       elif mlist[1]=='/submit':
          if not me(id):
               return
          postmsg='提交互助码太快,机器人判定无效操作,等待15秒执行提交操作,此时可以尝试其他命令.'
          bot_sendmsg(id,'提交违规',postmsg)
      elif mlist[0] not in command and mlist[1] not in command:
        if not me(id):
            return
        if mlist[0]==mlist[1]:
           postmsg=nm+'不要发送,重复内容...'
        else:
           postmsg='无效指令，请重新发送命令后按要求格式回复容' 
        bot_sendmsg(id,'提交功能',postmsg)
    if (postmsg):
        print('【输出日志】'+str(id)+nm+'-'+postmsg)
        
  except Exception as e:
      msg=str(e)
      print('bot_checkwrong'+msg)
def sendview(id):
   postmsg=bot_che()
   bot_sendmsg(id,'1.统计上车数据',postmsg)
   bot_sendmsg(id,'2.我提交的互助码',_viewcodeid(id))
   
      
def _addid(id):
   addok=False
   global hd_memjson 
   mecodelist=[]
   try:
     if id:
        if id not in hd_memjson.keys():
            hd_memjson[id]=[]
        if id in hd_memjson.keys():
           addok=True
     return addok
   except Exception as e:
       pass
       
def _addcodeid(id,code):#plus
   try:
     global hd_memjson
     mecodelist=hd_memjson[id]
     if id:
        if not code in mecodelist:
            mecodelist.append(code)
            hd_memjson[id]=mecodelist
        
   except Exception as e:
       pass
def _dellid(id):#plus
  ojbk=False
  global hd_memjson
  mecodelist=hd_memjson['id']
  try:
    if id:
      for data in hd_memjson[id]:
        mecodelist.append(data[2:len(data)])
      for data in hd_codelist:
         for sl in data:
             if sl in mecodelist:
                 data.remove(sl)
      ojbk=True
      for data in hd_codelist:
           for sl in data:
                   if sl in mecodelist:
                      ojbk=False
    return ojbk
  except Exception as e:
       pass
def _viewcodeid(id):
   view=[]
   try:
     if id:
        for key in hd_memjson.keys():
          if key==id:
              view=hd_memjson[id]
     
     return str(view)
   except Exception as e:
       pass

def _viewallid():
   try:
     allid=[]
     
     for key in hd_memjson.keys(): 
       allid.append(key)
     
     return str(allid)
     
   except Exception as e:
       pass

def _delcode(code):#plus
   boolres=False
   global hd_memjson
   mecodelist=[]
   try:
     for i in range(len(hd_codelist)):
        for da in hd_codelist[i]:
            if da==code:
               boolres=True
     for key in hd_memjson.keys(): 
         mecodelist=hd_memjson[key]
         if code in mecodelist:
            mecodelist.remove(code)
            hd_memjson[key]=mecodelist
     if boolres==True:
       for i in range(len(hd_codelist)):
         for da in hd_codelist[i]:
              if da==code:
                 hd_codelist[i].remove(da)
       for i in range(len(hd_codelist)):
         for da in hd_codelist[i]:
            if da==code:
               boolres=False
     return boolres
            	

   except Exception as e:
       pass
       
       
def me(id,x=0):
   try:
     permission=False
     if id:
        if id in hd_memjson.keys():
           permission=True
           if x==1:
             bot_sendmsg(id,bot_zhuce[2],'【'+str(id)+'】'+bot_zhuce[3])
             
        else:
           bot_sendmsg(id,bot_zhuce[0],'【'+str(id)+'】'+bot_zhuce[1])
           permission=False
     return permission
   except Exception as e:
       pass
def bot_admin(id,mlist,pop):
  try:
    postmsg=''
    tmplist=[]
    system=[]
    global reboot,reset
    system=tg_bot_cmd.strip().split('@')
    print('管理员数据验证====='+str(pop),mlist)
    if id!=tg_admin_id:
       return 
    if pop==2 or pop==1:
      if mlist[0]=='/admin_viewcode':
         if len(str(mlist[1]))>4:
            for data in hd_codelist:
               for da in data:
                 if da.find(mlist[1])>=0:
                     tmplist.append(da)
            postmsg='查询结果:'+str(tmplist)
         else:
            postmsg='检索字符太短'
         bot_sendmsg(tg_admin_id,'管理查询功能',postmsg)
      
      elif mlist[0]=='/admin_viewallid':
           print('查询所有ID\n')
           bot_sendmsg(tg_admin_id,'查询所有上车ID',_viewallid())
      elif mlist[0]=='/admin_addid':
         if len(str(mlist[1]))>4:
            if not str.isdigit(mlist[1]):
               bot_sendmsg(tg_admin_id,'管理加入ID功能','不是id吧，请重新输入数字id')
               return 
            if _addid(mlist[1]):
              bot_sendmsg(tg_admin_id,'管理加入ID功能','成功增加'+mlist[1])
            else:
              bot_sendmsg(tg_admin_id,'管理加入ID功能','权限ID加入失败'+mlist[1])
         else:
            postmsg='ID字符太短,可能错误.'
      elif mlist[0]=='/admin_delid':
         boolres=False
         if len(str(mlist[1]))>1:
           if _dellid(mlist[1]):
                 postmsg='删除所有id数据:'+'删除成功===.'
           else:
                postmsg='删除失败:ID数据不存在.'
         else:
            postmsg='检索ID字符太短,需要完整字符串.'
         bot_sendmsg(tg_admin_id,'管理删除ID功能',postmsg)
      elif mlist[0]=='/admin_delcode':
        
        if len(str(mlist[1]))>4:
          if delcode(mlist[1]):
               postmsg='查询结果:删除成功=====.'
          else:
              postmsg='查询结果:互助码不存在.'
        else:
          postmsg='检索code字符太短,需要完整字符串.'
        bot_sendmsg(tg_admin_id,'管理删除code功能',postmsg)
      elif mlist[0]=='/admin_reboot':
        if str(mlist[1])==system[1]:
             reboot=2
             postmsg='重启命令:正确'
        else:
              postmsg='重启命令:错误'
        
        bot_sendmsg(tg_admin_id,'管理重启功能',postmsg)
      elif mlist[0]=='/admin_reset':
        if str(mlist[1])==system[1]:
             reset=str(tg_bot_cmd)
             postmsg='清空数据开启'
             reset=2
             reboot=2
        else:
              postmsg='清空命令:错误'
        
        bot_sendmsg(tg_admin_id,'管理数据清空功能',postmsg)
  except Exception as e:
      msg=str(e)
      print('bot_admin'+msg)
          


def bot_che():
   print('\n统计缓存')
   other='\n统计缓存上车\n1.【上车人数】'+str(len(hd_memjson))+'\n'
   for i in range(len(hd_codelist)):
     other+='【'+str(i+1)+'】'+hd_nm[i][3:len(hd_nm[i])]+'互助码数:'+str(len(hd_codelist[i]))+'\n'
   print(ac_database+other)
   return ac_database+other
   
   
    
def tg_notice(x):
   if x==1 and r==2:
     bot_sendmsg(tg_group_id,'净网行动提示:','网警95327来了')
   elif x==2 and r==2:
      bot_sendmsg(tg_group_id,'净网行动提示:','网警95327暂时离开')
def bot_exit():
   print('程序退出写入数据中稍后🔔=======')
   print('检验数据:','数据文件个数:'+str(len(hd_codelist)+1),'活动个数:'+str(len(hd_nm)))
   bot_wr(hd_me[0][0:2],hd_me[0][3:len(hd_me[0])],hd_memjson)
   for i in range(len(hd_codelist)):
     bot_wr(hd_nm[i][0:2],hd_nm[i][3:len(hd_nm[i])],hd_codelist[i])
   print('程序结束🔔=======')
   
def bot_wr(hdnm,des,JDlist):
   try:
     JDjson={}
     JDjson['code']=200
     JDjson["2021"]="仅仅作为测试tg互助码思路,不做更新和解释,by红鲤鱼与绿鲤鱼与驴，2021.1.30"
     JDjson["Sort"]=hdnm+"数据"
     JDjson['Update_Time']=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
     if reset==1:
      if len(JDlist)>0:
        print(is_me(JDlist))
        
        if not is_me(JDlist):
             random.shuffle(JDlist)
        JDjson['data']=JDlist
        path=''
        if r==2:
          path='JD_TG/'
        with open("./"+path+hdnm+'.json',"w",encoding='utf8') as f:
          json.dump(JDjson,f)
          print(des+"数据写入文件完成...互助码个数:"+str(len(JDlist)))
      else:
        print(des+"数据获取为空，不写入...")
     if reset==2:
        JDlist=[]
        JDjson['data']=JDlist
        path=''
        if r==2:
          path='JD_TG/'
        with open("./"+path+hdnm+'.json',"w",encoding='utf8') as f:
          json.dump(JDjson,f)
          print(des+'清空数据库完毕')
        
     
        
   except Exception as e:
      msg=str(e)
      print(msg)

def bot_rd(hdnm,des):
   try:
     JDjson={}
     path=''
     xlist=''
     if r==2:
       path='JD_TG/'
     with open("./"+path+hdnm+'.json',"r",encoding='utf8') as f:
       JDjson=json.load(f)
       
       if JDjson['code']==200:
         if JDjson['data']==None:
             xlist=[]
         else:
             
             xlist=JDjson['data']
         print('读取'+des+'文件完成...个数:'+str(len(xlist)))
     
   except Exception as e:
      msg=str(e)
      print('bot_rd:'+msg)
      
   return xlist
def tm10():
   timeStamp=int(time.time())
   return timeStamp
def getpyramid():
  try:
   bbb=tg_ac_id.strip().split('@')
   res=requests.get(bbb[0],timeout=10000).text
   Sgls=re.compile('<span([\s\S]*?)<\/span>').findall(res)
   for i in range(len(Sgls)):
     data=re.compile('aria-label="([\s\S]*?)" href').findall(Sgls[i])
     if len(data)>0:
       zhjbzhenda.append(re.findall('\d+',data[0])[0])
     nm=Sgls[i].find('text-gray-light')
     if Sgls[i].find(bbb[2])>0 or Sgls[i].find(bbb[1])>0:
       data=Sgls[i][nm+17:len(Sgls[i])].strip()
     data2=re.compile(r'\d+m').findall(Sgls[i])
     data1=re.compile(r'\d+s').findall(Sgls[i])
     s=''
     if len(data1)>0:
        s+=data1[0]
     if len(data2)>0:
        s+=data2[0]
     if len(s)>0:
        if s not in zhjbzhenda:
           zhjbzhenda.append(s)
   
  except Exception as e:
      msg=str(e)
      print(msg)


def imallin():
   try:
    time.sleep(2)
    getpyramid()
    allin=False
    for i in range(len(zhjbzhenda)):
       if zhjbzhenda[2].find('s')>=0:
         allin=True
    if not allin:
       print('you need not be online....')
       bot_sendmsg(tg_admin_id,zhjbzhenda[0],'you need not be online....')
       exit()
    else:
      print('i am coming✌🏻️=====')
      bot_sendmsg(tg_admin_id,zhjbzhenda[0],'i am coming✌🏻️=====')
   except Exception as e:
      msg=str(e)
      
def is_me(x):
   try:
     ok=False
     json_object = json.loads(x)
     
   except Exception as e:
      msg=str(e)
      if msg.find('dict')>0:
        ok=True
   return ok

   
   
   
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
def read_sec(secret):
   globalid=''
   if secret in os.environ:
      globalid = os.environ[secret].strip()
   if secret in osenviron:
      globalid = osenviron[secret].strip()
   if not globalid:
       print(f'''【{secret}】 is empty,DTask is over.''')
   return globalid
def ac_load():
   global tg_bot_id,tg_member_id,tg_group_id,tg_bot_cmd,tg_new_id,tg_admin_id,tg_ac_id

   tg_bot_id=read_sec('tg_bot_id')
   tg_member_id=read_sec('tg_member_id')
   tg_group_id=read_sec('tg_group_id')
   tg_bot_cmd=read_sec('tg_bot_cmd')
   tg_new_id=read_sec('tg_new_id')
   tg_admin_id=read_sec('tg_admin_id')
   tg_ac_id=read_sec('tg_ac_id')
   if not tg_admin_id or not tg_ac_id or not tg_bot_id:
        exit()
def bot_trans():
  try:
   for i in range(heartnum):
    ac_load()
    if reboot==2:
        print('接受命令,退出.......')
        break
    bot_loadmsg()
    bot_chat()
    print('【'+str(i+1)+'】次运行完毕=======')
    print('心跳包运行中.....稍等'+str(bot_timeout)+'秒')
    time.sleep(bot_timeout)
  except Exception as e:
      msg=str(e)
      print(msg)
      



@clock
def start():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   bot_load()
   ac_load()
   imallin()
   tg_notice(1)
   bot_trans()
   bot_exit()
   tg_notice(2)
if __name__ == '__main__':
       start()
