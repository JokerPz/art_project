#coding:utf8
import tornado.web
import json
import os
import datetime
import uuid

class LoginHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        self.render("admin/login.html")

    def post(self,*args,**kwargs):
        name = self.get_argument("name",'')
        pwd = self.get_argument("pwd",'')
        _xsrf = self.get_argument("_xsrf")
        print("_xsrf:"+str(_xsrf))
        res = dict(
            ok=1
        )
        if name =='':
            res['ok'] = 0
            res['name'] = "管理员账号不能为空"
        if pwd == '':
            res['ok'] = 0
            res['pwd'] = "管理员密码不能为空"
        if res['ok']== 1:
            import hashlib
            up = hashlib.md5()
            up.update(pwd.encode("utf8"))#  这里需要注意一下
            pwd = up.hexdigest()
            # print('pwd:'+str(pwd))
            sql = "select count(*) from admin where name = '%s' and pwd = '%s' " % (name,pwd)
            count = self.db.execute(sql).fetchone()
            if count [0] ==0:
                print("count[0]:"+str(count[0]))
                res['ok']=0
                print("res['ok']:"+str(res['ok']))
                res['pwd']="账号或者密码错误！"
            else:
                self.set_secure_cookie("username",name)
        self.set_header("content-type","application/json")
        self.write(json.dumps(res))

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect('/login.html')
class AdminHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        return self.get_secure_cookie("username")        

class TaglistHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        key = self.get_argument('key','')#搜索关键字
        page = self.get_argument('page',1)
        page = int(page)
        print("检测错误1："+"aaaaa"+key+"aaa"+str(page))        
        sql = "select count(*) from tag where name like :key"
        total = self.db.execute(sql,dict(key='%'+key+'%')).fetchone()[0]
        shownum = 10 # 每页列表显示的条数
        import math
        pagenum = int(math.ceil(total/shownum))
        if pagenum == 0:
            pagenum = 1
        print("检测错误2："+"aaaaa"+str(pagenum)+"aaa"+str(page))
        if page<1 :
            self.redirect(self.request.path + "?page = %d&key = %s" % (1,key))
        if page>pagenum:
            self.redirect(self.request.path + "?page = %d&key = %s" % (pagenum,key))
        offset = (page-1)*int(shownum)
        sql = "select id,name,addtime from tag where name like :key limit :offset,:limit"
        data = self.db.execute(sql,dict(key='%'+key+'%',offset=offset,limit=int(shownum))).fetchall()
        btnnum = 5 #列表的显示页码数目
        print("检测错误3："+"aaaaa"+str(pagenum)+"aaa"+str(page))
        if btnnum>pagenum:
            firstpage = 1
            lastpage = pagenum
        else:
            if page ==1:
                firstpage =1
                lastpage =btnnum
            else:
                firstpage = page-2
                lastpage = page+btnnum -3
                if firstpage <1:
                    firstpage =1
                if lastpage >pagenum:
                    lastpage = pagenum
        
        prev = page-1
        next = page+1
        if prev<1:
            prev=1
        if next>pagenum:
            next = pagenum
        arr = dict(
            pagenum = pagenum,
            total = total,
            prev = prev,
            next = next,
            pagerange = range(firstpage,lastpage+1),#索引到前一位
            data=data,
            url = self.request.path,
            key=key,
            page=page
        )
        self.db.commit()
        self.db.close()
        self.render("admin/tag_list.html",arr=arr)

class TageditHandler(AdminHandler):
    @tornado.web.authenticated    
    def get(self):
        id = self.get_argument("id",None)
        if id!=None:
            id = int(id)
            sql = "select id,name,info from tag where id = :id"
            tag = self.db.execute(sql,dict(id=id)).fetchone()
            self.db.commit()
            self.db.close()
            self.render("admin/tag_edit.html",tag=tag,id= id)
        else:
            self.render("admin/tag_edit.html",id=id)
            

    def post(self,*args,**kwargs):
        name = self.get_argument("name",'')
        info = self.get_argument("info",'')
        id = self.get_argument("id",'')
        print("id:"+id)
        res = dict(
            ok=1
        )
        if id !='':
            if name =='':
                res['ok']=0
                res['name']= '标签名称不能为空！'
            if info =='':
                res['ok']=0
                res['info']= '编辑信息不能为空！'
            if res['ok']==1:
                if int(id) ==0:
                    sql = "insert into tag(name,info) values('%s','%s')" % (name,info)
                else:
                    sql = "update tag set name='%s',info='%s' where id=%d " % (name,info,int(id))
                self.db.execute(sql)#提交查询语句
                self.db.commit()
                self.db.close()
            self.set_header("content-type","application/json")
            self.write(json.dumps(res))

class TagdelHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        id = int(id)
        sql = "delete from tag where id = :id" 
        self.db.execute(sql,dict(id = id))
        self.db.commit()
        self.db.close()
        self.redirect("/tag_list.html")

class ArtlistHandler(AdminHandler):
    @tornado.web.authenticated    
    def get(self):
        key = self.get_argument('key','')#搜索关键字
        page = self.get_argument('page',1)
        page = int(page)
        sql = "select count(*) from art where title like :key or content like :key or info like :key"
        total = self.db.execute(sql,dict(key='%'+key+'%')).fetchone()[0]
        shownum = 10 # 每页列表显示的条数
        import math
        pagenum = int(math.ceil(total/shownum))
        if page<1 :
            self.redirect(self.request.path + "?page = %d&key = %s" % (1,key))
        if page>pagenum:
            self.redirect(self.request.path + "?page = %d&key = %s" % (pagenum,key))
        offset = (page-1)*int(shownum)
        sql = "select a.id,a.title,a.img,t.name,a.addtime from art a left join tag t on a.tag = t.id where  a.title like :key or a.content like :key or a.info like :key limit :offset,:limit"
        data = self.db.execute(sql,dict(key='%'+key+'%',offset=offset,limit=int(shownum))).fetchall()
        btnnum = 5 #列表的显示页码数目
        if btnnum>pagenum:
            firstpage = 1
            lastpage = pagenum
        else:
            if page ==1:
                firstpage =1
                lastpage =btnnum
            else:
                firstpage = page-2
                lastpage = page+btnnum -3
                if firstpage <1:
                    firstpage =1
                if lastpage >pagenum:
                    lastpage = pagenum
        
        prev = page-1
        next = page+1
        if prev<1:
            prev=1
        if next>pagenum:
            next = pagenum
        arr = dict(
            pagenum = pagenum,
            total = total,
            prev = prev,
            next = next,
            pagerange = range(firstpage,lastpage+1),#索引到前一位
            data=data,
            url = self.request.path,
            key=key,
            page=page
        )
        self.db.commit()
        self.db.close()
        self.render("admin/art_list.html",arr=arr)

class ArteditHandler(AdminHandler):
    @tornado.web.authenticated    
    def get(self):
        sql = "select id,name from tag"
        tags = self.db.execute(sql)
        self.db.commit()
        self.db.close()
        id = self.get_argument("id",None)
        if id!=None:
            id = int(id)
            sql = "select id,title,info,content,tag,img from art where id = :id"
            art = self.db.execute(sql,dict(id=id)).fetchone()
            self.db.commit()
            self.db.close()
            self.render("admin/art_edit.html",tags=tags,id = id,art=art)
        else:
            self.render("admin/art_edit.html",tags=tags,id = id)

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        title = self.get_argument("title",'')
        info = self.get_argument("info",'')
        content = self.get_argument("content",'')
        img = self.get_argument("img",'')
        tag = self.get_argument("tag",'')
        id = self.get_argument("id",'')
        print("tag:"+str(tag))
        res = dict(ok = 1)
        if title == '':
            res['ok']=0
            res['title'] = "文章标题不能为空！"
        if info == '':
            res['ok']=0
            res['info'] = "文章简介不能为空！"  
        if content == '':
            res['ok']=0
            res['content'] = "文章内容不能为空！"  
        if img == '':
            res['ok']=0
            res['img'] = "文章封面不能为空！"
        if tag == '' or int(tag)==0:
            res['ok']=0
            res['tag'] = "文章标签不能为空！"
        if res['ok'] == 1:
            if int(id)==0:
                sql = "insert into art(title,info,content,img,tag) values(:a,:b,:c,:d,:e)"
                self.db.execute(sql,dict(a=title,b=info,c=content,d=img,e=int(tag)))
            else:
                sql = "update art set title=:a,info=:b,content=:c,img=:d,tag=:e where id = :id"
                self.db.execute(sql,dict(a=title,b=info,c=content,d=img,e=int(tag),id=int(id)))
            self.db.commit()
            self.db.close()
        self.set_header("content-type","application/json")
        self.write(json.dumps(res))
        

class UpHandler(AdminHandler):
    def check_xsrf_cookie(self):
        return True

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        files = self.request.files["img"]
        imgs = []
        upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"static/uploads")
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        for v in files:
            prefix1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            prefix2 = uuid.uuid4().hex
            newname = prefix1+prefix2 + os.path.splitext(v["filename"])[-1]
            with open(upload_path+'/'+newname,"wb") as up:
                up.write(v["body"])
            imgs.append(newname)
            # imgs.append(v["filename"])
        
        res = dict(ok = 1,img=imgs[0])
        self.set_header("content-type","application/json")
        self.write(json.dumps(res))

class ArtdelHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        id = int(id)
        sql = "delete from art where id = :id" 
        self.db.execute(sql,dict(id = id))
        self.db.commit()
        self.db.close()
        self.redirect("/art_list.html")