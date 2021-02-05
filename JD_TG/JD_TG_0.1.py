# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : TG Bot
   Author   : 红鲤鱼与绿鲤鱼与驴
   date     : 2021-2-2 21:32 
   Desc     : 公众号iosrule,编程测试与学习
   Gamerule: Tg群，微信学习，请勿用于非法用途
   update: 1.2021.2.4 修复管理员删除字符bug,修复下超时重置清0.2.修复超时逻辑判断，添加改版前上车人数据代码。调整活动简称。
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
longid=0
upid=0
reboot=''
#远程配置
heartnum=100
r=2



ac_database=''
osenviron={}
telelist=[]
result=''
msglist=[]
uslist=[]






#=====================================
command=['/help','/submit','/start','/admin_delid','/admin_delcode','/admin_viewcode','/admin_reboot']
description=['帮助功能:','提交功能','圈友查询','管理员删除数据库群友id','管理员删除互助码','管理员查询互助码','管理员重启机器人']
hd_nm=['ID@圈友ID','NC@农场','NS@年兽','MC@萌宠','JC@惊喜工厂','DC@京东工厂','ZD@种豆']
hd_codelist=[]
bot_timeout=15
bot_fix=0
fixtime=15
#=====================================
def help_update():
   help=''
   try:
      help+='2.当前互助码活动(动态更新中):'+str(hd_nm)+'\n'
      return help
   except Exception as e:
      pass


      
      
def bot_load():
   global hd_codelist
   try:
      for ll in hd_nm:
        hd_codelist.append(bot_rd(ll[0:2],ll[3:len(ll)]))
      ac_data()
   except Exception as e:
      msg=str(e)
      print('bot_loadfile'+msg)
      
      
def ac_data():
   try:
      global ac_database
      print('\n成功上车人数')
      ac_database='1.【成功上车人数】'+str(len(hd_codelist[0]))+'\n'
      for i in range(1,len(hd_codelist)):
        ac_database+='【'+hd_nm[i][3:len(hd_nm[i])]+'互助码数】'+str(len(hd_codelist[i]))+'\n'
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
      global msglist
      username=''
      msgtext=''
      msglist=[]
      res=bot_update()
      
      if not 'result' in res:
        print('退出')
        return 
      if len(res['result'])==0:
        print('退出')
        return 
      i=0
      username=''
      for data in res['result']:
        i+=1
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
          
          
        
      print('圈友人数:'+str(len(msglist)))
      #print(msglist)
   except Exception as e:
      msg=str(e)
      print('bot_loadmsg'+msg)
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
          print('【会话+'+str(i+1)+'+】超时'+str(checktm)+'检验:'+str(bot_fix))
          
          if checktm>bot_timeout*2+5+bot_fix:
             print('机器人接收上个信息超时.....')
             bot_fix=0
             continue
             
          if len(msglist[i])>4:
            
            newmsglist.append(mm1.strip())
            newmsglist.append(mm2.strip())
            bot_checkwrong(id,nm,newmsglist,2)
            bot_admin(id,newmsglist,2)
          
          	
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
    print('通用数据验证=====',mlist)
    if pop==1:
       
       if mlist[0]=='/help':
          postmsg='1.京东互助码提交机器人测试中，请在对话框输入字符 /  查看对应指令再发送内容。每个京东活动互助码分开提交,格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556\n'+help_update()
          bot_sendmsg(id,'帮助功能',postmsg)
       elif mlist[0]=='/start':
          postmsg=bot_che()
          bot_sendmsg(id,'统计功能',postmsg)
    elif pop==2:
      
      if mlist[0] in command and mlist[1] in command:
        for i in range(2):
           if mlist[i]=='/help':
             postmsg='京东互助码提交机器人测试中，请在对话框输入字符 /  查看对应指令再发送内容。每个京东活动互助码分开提交,格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556\n'+help_update()
             bot_sendmsg(id,'帮助功能',postmsg)
           elif mlist[i]=='/start':
               postmsg=bot_che()
               bot_sendmsg(id,'统计功能',postmsg)
      elif mlist[0] in command and mlist[1] not in command:
        if mlist[0]=='/submit':
          i=0
          
          for ll in hd_nm:
            i+=1
            print('check hd:'+ll[0:2])
            if mlist[1].find(ll[0:2])==0:
               print('add======')
               postmsg=mlist[1][2:len(mlist[1])]
               print('get code:'+postmsg)
               allnum=len(postmsg.strip().split('@'))
               for code in postmsg.strip().split('@'):
                 if code in hd_codelist[i-1]:
                   print('数据库重复数据，跳过====')
                   allnum-=1
                   continue
                 hd_codelist[i-1].append(code)
               postmsg=ll[3:len(ll)]+'活动共计提交'+str(len(postmsg.strip().split('@')))+'个互助码,其中'+str(allnum)+'个为有效互助码，其他为重复数据,1个小时后更新进数据库....'
               _addid(id)
               break
            else:
               postmsg=nm+'请勿发送无效互助码....格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556'
          bot_sendmsg(id,'提交功能',postmsg)
        elif mlist[0]=='/help':
             postmsg='京东互助码提交机器人测试中，请在对话框输入字符 /  查看对应指令再发送内容。每个京东活动互助码分开提交,格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556\n'+help_update()
             bot_sendmsg(id,'帮助功能',postmsg)
        elif mlist[0]=='/start':
               postmsg=bot_che()
               bot_sendmsg(id,'查询功能',postmsg)
      elif mlist[0] not in command and mlist[1] in command:
       if mlist[1]=='/help':
          postmsg='京东互助码提交机器人测试中，请在对话框输入字符 /  查看对应指令再发送内容。每个京东活动互助码分开提交,格式:活动简称大写字母+互助码,多个互助码用@连接,例如京东农场NC12333@885666@8556\n'+help_update()
          bot_sendmsg(id,'查询功能',postmsg)
       elif mlist[1]=='/start':
          postmsg=bot_che()
          bot_sendmsg(id,'统计功能',postmsg)
       elif mlist[1]=='/submit':
          postmsg='提交互助码太快,机器人判定无效操作,等待15秒执行提交操作,此时可以尝试其他命令.'
          bot_sendmsg(id,'提交违规',postmsg)
      elif mlist[0] not in command and mlist[1] not in command:
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

      
def _addid(id):
   global hd_codelist
   try:
     if id:
        if not str(id) in hd_codelist[0]:
            hd_codelist[0].append(str(id))
   except Exception as e:
       pass
       
       
       
def bot_admin(id,mlist,pop):
  try:
    postmsg=''
    tmplist=[]
    global reboot
    print('管理员数据验证=====',mlist)
    if id!=tg_admin_id:
       return 
    if pop==2:
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
      elif mlist[0]=='/admin_delid':
         boolres=False
         if len(str(mlist[1]))>4:
            for data in hd_codelist[0]:
                   if data==mlist[1]:
                      boolres=True
            if boolres==True:
              for data in hd_codelist[0]:
                   if data==mlist[1]:
                     hd_codelist[0].remove(data)
              for data in hd_codelist[0]:
                   if data==mlist[1]:
                      boolres=False
              if boolres==False:
                 postmsg='查询结果:'+'删除失败.'
              else:
                 postmsg='查询结果:'+'删除成功===.'
            else:
                postmsg='查询结果:ID不存在.'
         else:
            postmsg='检索ID字符太短,需要完整字符串.'
         bot_sendmsg(tg_admin_id,'管理删除ID功能',postmsg)
      elif mlist[0]=='/admin_delcode':
        boolres=False
        if len(str(mlist[1]))>4:
          for i in range(1,len(hd_codelist)):
            for da in hd_codelist[i]:
              if str(da)==str(mlist[1]):
                 boolres=True
          if boolres==True:
            for i in range(1,len(hd_codelist)):
               for da in hd_codelist[i]:
                 if da==mlist[1]:
                      hd_codelist[i].remove(da)
            for i in range(1,len(hd_codelist)):
               for da in hd_codelist[i]:
                 if str(da)==str(mlist[1]):
                     boolres=False
            if boolres==False:
               postmsg='查询结果:删除失败.'
            else:
               postmsg='查询结果:删除成功=====.'
          else:
              postmsg='查询结果:互助码不存在.'
        else:
          postmsg='检索code字符太短,需要完整字符串.'
        bot_sendmsg(tg_admin_id,'管理删除code功能',postmsg)
      elif mlist[0]=='/admin_reboot':
        if str(mlist[1])==str(tg_bot_cmd):
             reboot=str(tg_bot_cmd)
             postmsg='重启命令:正确'
        else:
              postmsg='重启命令:错误'
        print(postmsg)
        bot_sendmsg(tg_admin_id,'管理重启功能',postmsg)
  except Exception as e:
      msg=str(e)
      print('bot_admin'+msg)
          

def msg_clean(msg,ckmsg):
   try:
     xlist=[]
     fn=msg.find('submit+')
     msg=msg.strip()[fn+7:len(msg)]
     if msg.find(ckmsg)>=0:
       s1=msg.strip().split('\n')
       for i in s1:
         if i.find(ckmsg)==0:
           i=i[2:len(i)]
           s2=i.split('@')
           for j in s2:
            if j in xlist:
               continue
            xlist.append(j)
     if len(xlist)>0:
       return xlist
   except Exception as e:
      msg=str(e)
      print('msg_clean'+msg)
def bot_che():
   print('\n统计上车')
   other='\n2.【当前总上车人数】'+str(len(hd_codelist[0]))+'\n'
   for i in range(1,len(hd_codelist)):
     other+='【'+hd_nm[i][3:len(hd_nm[i])]+'互助码数】'+str(len(hd_codelist[i]))+'\n'
   print(ac_database+other)
   return ac_database+other


    
def tg_notice(x):
   if x==1 and r==2:
     bot_sendmsg(tg_group_id,'净网行动提示:','网警95327来了')
   elif x==2 and r==2:
      bot_sendmsg(tg_group_id,'净网行动提示:','网警95327暂时离开')

def bot_wr(hdnm,des,JDlist):
   try:
     JDjson={}
     random.shuffle(JDlist)
     JDjson['code']=200
     JDjson['data']=JDlist
     JDjson["2021"]="仅仅作为测试tg互助码思路,不做更新和解释,by红鲤鱼与绿鲤鱼与驴，2021.1.30"
     JDjson["Sort"]=hdnm+"数据"
     
     JDjson['Update_Time']=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
     if len(JDlist)>0:
        path=''
        if r==2:
          path='JD_TG/'
        with open("./"+path+hdnm+'.json',"w",encoding='utf8') as f:
          json.dump(JDjson,f)
          print(des+"数据写入文件完成...互助码个数:"+str(len(JDlist)))
     else:
        print(des+"数据获取为空，不写入...")
   except Exception as e:
      msg=str(e)
      print(msg)

def bot_rd(hdnm,des):
   try:
     JDjson={}
     xlist=[]
     path=''
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
      xlist=[]
   return xlist
def tm10():
   timeStamp=int(time.time())
   return timeStamp
   
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
   global tg_bot_id,tg_member_id,tg_group_id,tg_bot_cmd,tg_new_id,tg_admin_id

   tg_bot_id=read_sec('tg_bot_id')
   tg_member_id=read_sec('tg_member_id')
   tg_group_id=read_sec('tg_group_id')
   tg_bot_cmd=read_sec('tg_bot_cmd')
   tg_new_id=read_sec('tg_new_id')
   tg_admin_id=read_sec('tg_admin_id')
   if not tg_admin_id:
        exit()
def bot_trans():
  try:
   for i in range(heartnum):
    ac_load()
    if reboot==str(tg_bot_cmd):
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
      

def bot_exit():
   print('程序退出写入数据中稍后🔔=======')
   print('检验数据:','活动列表个数:'+str(len(hd_codelist)),'活动个数:'+str(len(hd_nm)))
   for i in range(len(hd_codelist)):
     bot_wr(hd_nm[i][0:2],hd_nm[i][3:len(hd_nm[i])],hd_codelist[i])
   print('程序结束🔔=======')
@clock
def start():
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   bot_load()
   ac_load()
   tg_notice(1)
   bot_trans()
   bot_exit()
   tg_notice(2)
if __name__ == '__main__':
       start()
