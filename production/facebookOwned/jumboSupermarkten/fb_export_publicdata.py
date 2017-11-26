#dependencies
import urllib2
import json
from datetime import datetime
from datetime import date
from datetime import timedelta
#import MySQLdb as mdb

#Open access_data file
with open('access_data.json', 'r') as fp:
    fb_data = json.load(fp)

fb_access_token = fb_data["app_access_token"]
fb_app_id = fb_data["app_id"]
fb_app_secret = fb_data["app_secret"]

#Database connection info
con_ip = "95.85.56.92"
con_db = "prepmetrics_db"
con_user = "preper"
con_pass = "passa1sdE!fs0!metrics"

#cache general variables
current_date_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now()
last_week_date = (current_date - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
yesterday_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

#pages to scrape
api_accounts = ["jumbosupermarkten","PLUSsupermarkt","EMTESUPERMARKTEN","Dirksupermarkten","CoopSupermarkten","lidlnederland","JanLindersSupermarkten","DEENSupermarkten","albertheijn"]
page_loop = 0

for page in api_accounts:
    #http api call constructor
    api_base = "https://graph.facebook.com"
    api_version = "v2.10"
    api_page = api_accounts[page_loop]
    api_post_limit = "16"
    api_comment_limit = "1500"
    api_like_limit = "6000"
    api_fields = "id,name,posts.limit("+api_post_limit+"){comments.limit("+api_comment_limit+"){message,id,comment_count,created_time,like_count},caption,likes.limit("+api_like_limit+"),timeline_visibility,message,shares,type,created_time},fan_count,talking_about_count,were_here_count"
    api_construct = api_base+"/"+api_version+"/"+api_page+"?fields="+api_fields+"&access_token="+fb_access_token
    print(api_construct)

    #make api request based on constructed data
    api_response = urllib2.urlopen(api_construct,timeout=15)
    response_string = api_response.read().decode('utf-8')
    json_data = json.loads(response_string)

    #variables for cumulative calculations
    post_like_total = 0
    post_comment_total = 0
    post_share_total = 0

    post_loop = 0
    for posts in json_data["posts"]["data"]:
        if json_data["posts"]["data"][post_loop]["created_time"][:10] == last_week_date[:10]:
            post_message = ""
            post_comments_count = 0
            post_likes_count = 0
            post_share_count = 0
            if "message" in json_data["posts"]["data"][post_loop]:
                post_message = json_data["posts"]["data"][post_loop]["message"]
            if "comments" in json_data["posts"]["data"][post_loop]:
                post_comments_count = len(json_data["posts"]["data"][post_loop]["comments"]["data"])
            if "likes" in json_data["posts"]["data"][post_loop]:
                post_likes_count = len(json_data["posts"]["data"][post_loop]["likes"]["data"])
            if "shares" in json_data["posts"]["data"][post_loop]:
                post_share_count = json_data["posts"]["data"][post_loop]["shares"]["count"]
            post_obj = {
                "scrape_date": current_date_timestamp,
                "page_id": json_data["id"],
                "page_name": json_data["name"],
                "post_id": json_data["posts"]["data"][post_loop]["id"],
                "post_type": json_data["posts"]["data"][post_loop]["type"],
                "post_created_time": json_data["posts"]["data"][post_loop]["created_time"][:-5].replace("T"," "),
                "post_message": post_message.encode('utf8'),
                "post_timeline_visibility": json_data["posts"]["data"][post_loop]["timeline_visibility"],
                "post_comment_count": post_comments_count,
                "post_like_count": post_likes_count,
                "post_share_count": post_share_count
            }
            print(post_obj)
            add_post = ("INSERT INTO fb_posts "
                "(scrape_date, page_id, page_name, post_id, post_type, post_created_time, post_message, post_timeline_visibility, post_comment_count, post_like_count, post_share_count)"
                "VALUES (%(scrape_date)s, %(page_id)s, %(page_name)s, %(post_id)s, %(post_type)s, %(post_created_time)s, %(post_message)s, %(post_timeline_visibility)s, %(post_comment_count)s, %(post_like_count)s, %(post_share_count)s)")

            #Setup database connection
            #con = mdb.connect(con_ip, con_user, con_pass, con_db)
            #with con:
            #    cur = con.cursor()
            #    cur.execute(add_post, post_obj)

            #    con.commit()

            #con.close()

            if post_comments_count > 0:
                comment_loop = 0
                if "comments" in json_data["posts"]["data"][post_loop]:
                    for comments in json_data["posts"]["data"][post_loop]["comments"]["data"]:
                        post_comment_obj = {
                            "scrape_date": current_date_timestamp,
                            "page_id": json_data["id"],
                            "post_id": json_data["posts"]["data"][post_loop]["id"],
                            "comment_id": json_data["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["id"],
                            "comment_created_time": json_data["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["created_time"][:-5].replace("T"," "),
                            "comment_message": json_data["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["message"].encode('utf8'),
                            "comment_like_count": json_data["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["like_count"],
                            "comment_comment_count": json_data["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["comment_count"],
                        }
                        print(post_comment_obj)

                        #Configure the format of sending data to database
                        add_comment = ("INSERT INTO fb_comments "
                            "(scrape_date, page_id, post_id, comment_id, comment_created_time, comment_message, comment_like_count, comment_comment_count)"
                            "VALUES (%(scrape_date)s, %(page_id)s, %(post_id)s, %(comment_id)s, %(comment_created_time)s, %(comment_message)s, %(comment_like_count)s, %(comment_comment_count)s)")

                        #Setup database connection
                        #con = mdb.connect(con_ip, con_user, con_pass, con_db)
                        #with con:
                        #    cur = con.cursor()
                        #    cur.execute(add_comment, post_comment_obj)

                        #    con.commit()

                        #con.close()
                        comment_loop = comment_loop+1
                        print("posted")

        post_comments_base = 0
        post_likes_base = 0
        post_share_base = 0

        if "comments" in json_data["posts"]["data"][post_loop]:
                post_comments_base = len(json_data["posts"]["data"][post_loop]["comments"]["data"])
        if "likes" in json_data["posts"]["data"][post_loop]:
                post_likes_base = len(json_data["posts"]["data"][post_loop]["likes"]["data"])
        if "shares" in json_data["posts"]["data"][post_loop]:
                post_share_base = json_data["posts"]["data"][post_loop]["shares"]["count"]

        if post_loop < 10:
            post_like_total = post_like_total + post_comments_base
            post_comment_total = post_comment_total + post_likes_base
            post_share_total = post_share_total + post_share_base
            print(post_like_total)
        post_loop = post_loop+1

    page_new_fans = 0
    page_new_here = 0
    page_new_talks = 0

    #con = mdb.connect(con_ip, con_user, con_pass, con_db)
    #with con:
    #    cur = con.cursor()
    #    query = ("SELECT page_name,page_id, page_fan_count, page_were_here_count, page_talking_about_count FROM fb_pagedata "
    #        "WHERE scrape_date BETWEEN %s AND %s")
    #    start = yesterday_date[:10]+" 00:00:00"
    #    end = yesterday_date[:10]+" 23:59:59"

    #    que = cur.execute(query, (start, end))
    #    if que != 0:
    #	    result = cur.fetchall()
    #	    print(que)
    #	    print(result)
    #	    for row in result:
    #    	    if row[1] == json_data["id"]:
    #			    print(row[0])
    #                page_new_fans = json_data["fan_count"]-row[2]
    #                page_new_here = json_data["were_here_count"]-row[3]
    #                page_new_talks = json_data["talking_about_count"]-row[4]
    #    cur.close()
    #con.close()

    page_obj = {
        "scrape_date": current_date_timestamp,
        "page_id": json_data["id"],
        "page_name": json_data["name"],
        "page_fan_count": json_data["fan_count"],
        "page_were_here_count": json_data["were_here_count"],
        "page_talking_about_count": json_data["talking_about_count"],
        "post_like_total": post_like_total,
        "post_comment_total": post_comment_total,
        "post_share_total": post_share_total,
        "page_new_fans": page_new_fans,
        "page_new_here": page_new_here,
        "page_new_talks": page_new_talks
    } #IMP and other interaction scores # APM and other acquisition scores

    add_pagedata = ("INSERT INTO fb_pagedata "
        "(scrape_date, page_id, page_name, page_fan_count, page_were_here_count, page_talking_about_count, post_like_total, post_comment_total, post_share_total, page_new_fans, page_new_here, page_new_talks)"
        "VALUES (%(scrape_date)s, %(page_id)s, %(page_name)s, %(page_fan_count)s, %(page_were_here_count)s, %(page_talking_about_count)s, %(post_like_total)s, %(post_comment_total)s, %(post_share_total)s, %(page_new_fans)s, %(page_new_here)s, %(page_new_talks)s)")

    #Setup database connection
    #con = mdb.connect(con_ip, con_user, con_pass, con_db)
    #with con:
    #    cur = con.cursor()
    #    cur.execute(add_pagedata, page_obj)

    #    con.commit()

    #con.close()
    page_loop = page_loop+1