import urllib2
import json
import prepLogger

#prepApp
app_name = "httpErrorHandling.py"
py_version = "2.7"
creator = "prepmetrics"

#Setup logger for app
logger = prepLogger.setup_custom_logger(app_name)
logger.debug('start app: '+ app_name)

def error_handling():
    request_uri = urllib2.Request('https://graph.faceblook.com/v2.10/jumbosupermarkten?fields=id,name,posts.limit(16){comments.limit(1500){message,id,comment_count,created_time,like_count},caption,likes.limit(6000),timeline_visibility,message,shares,type,created_time},fan_count,talking_about_count,were_here_count&access_token=189107884825866|GAK5u63gwXIlsjijOhxh5iTZeqo')
    try:
        api_response = urllib2.urlopen(request_uri, timeout=30)
        response_string = api_response.read().decode('utf-8')
        json_data = json.loads(response_string)
        print("success")
        logger.debug('data collected: '+ 'request_type')
    except urllib2.HTTPError, err:
        if err.code == 404:
            print("Page not found!")
            logger.error("Page not found!")
        elif err.code == 403:
            print "Access denied!"
            logger.error('Access denied!')
        elif err.code == 500:
            print "Timeout error!"
            logger.error('Timeout error!')
        else:
            print "Something happened! Error code", err.code
            logger.error(err.code)
    except urllib2.URLError, err:
        print "Some other error happened:", err.reason
        logger.error(err.reason)

def main():
    error_handling()
    logger.debug('end app: '+ app_name)

if __name__ == '__main__':
    main()