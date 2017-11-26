import urllib2
import json
import sys
sys.path.append('../prepModules')
from prepLogger import appLogger
from prepHttp import httpJson

#prepApp
app_name = "httpErrorHandling"
py_version = "2.7"
creator = "prepmetrics"

#Setup logger for app
logger = appLogger(app_name)
logger.debug('start app: '+ app_name)

def getdata():
    crawl_url = 'https://graph.facebook.com/v2.10/jumbosupermarkten?fields=id,name,posts.limit(16){comments.limit(1500){message,id,comment_count,created_time,like_count},caption,likes.limit(6000),timeline_visibility,message,shares,type,created_time},fan_count,talking_about_count,were_here_count&access_token=189107884825866|GAK5u63gwXIlsjijOhxh5iTZeqo'
    respons = httpJson(app_name, crawl_url, 30)
    print(respons)

def main():
    getdata()
    logger.debug('end app: '+ app_name)

if __name__ == '__main__':
    main()