#coding:utf8
import os
base_dir = os.path.dirname(__file__)

configs = dict(
    template_path = os.path.join(base_dir,"templates"),
    static_path = os.path.join(base_dir,"static"),
    debug = True,
    xsrf_cookies = True,
    cookie_secret = "8a6ee410cddc4cb7b79f4d22fbca2b47",
    login_url ="/login.html"
)