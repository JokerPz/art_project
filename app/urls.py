#coding: utf8
from app.home.views import IndexHandler as home_index
from app.home.views import SearchHandler as home_search
from app.home.views import DetailHandler as home_detail

home_urls = [
    (r"/",home_index),
    (r"/index\.html",home_index),
    (r"/search\.html",home_search),
    (r"/detail\.html",home_detail)
]

from app.admin.views import LoginHandler as admin_login
from app.admin.views import TaglistHandler as admin_taglist
from app.admin.views import TageditHandler as admin_tagedit
from app.admin.views import ArtlistHandler as admin_artlist
from app.admin.views import ArteditHandler as admin_artedit
from app.admin.views import LogoutHandler as admin_logout
from app.admin.views import TagdelHandler as admin_tagdel
from app.admin.views import UpHandler as admin_upload
from app.admin.views import ArtdelHandler as admin_artdel

admin_urls= [
    (r"/login\.html",admin_login),
    (r"/tag_list\.html",admin_taglist),
    (r"/tag_edit\.html",admin_tagedit),
    (r"/tag_del\.html",admin_tagdel),
    (r"/art_list\.html",admin_artlist),
    (r"/art_edit\.html",admin_artedit),
    (r"/art_del\.html",admin_artdel),
    (r"/logout\.html",admin_logout),
    (r"/upload",admin_upload),
    (r"/art_del\.html",admin_artdel),
]

urls = home_urls + admin_urls