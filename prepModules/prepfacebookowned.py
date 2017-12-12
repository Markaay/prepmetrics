"""all functions for retrieving owned facebook data through the facebook graph api"""
#from prepModules.preplogger import applogger
#classes for public facebook owned data and private owned page data

def fb_httpbuilderpublic(app, pageid, postlimit, commentlimit, likelimit, accesstoken):
    """function that forms the hhtp request url based on input"""
    from preplogger import applogger
    logger = applogger(app)
    #constructor for exporting public facebook graph api data
    api_base = "https://graph.facebook.com"
    api_version = "v2.11"
    api_page = str(pageid)
    api_post_limit = str(postlimit)
    api_comment_limit = str(commentlimit)
    api_like_limit = str(likelimit)
    api_fields = "id,name,posts.limit("+api_post_limit+"){comments.limit("+api_comment_limit+"){message,id,comment_count,created_time,like_count},caption,likes.limit("+api_like_limit+"),timeline_visibility,message,shares,type,created_time},fan_count,talking_about_count,were_here_count"
    api_construct = api_base+"/"+api_version+"/"+api_page+"?fields="+api_fields+"&access_token="+accesstoken
    logger.debug('FB API request constructed: '+ api_construct)
    return api_construct

def fb_gettoken(app, app_id, app_secret, data_location):
    """function to retrieve new app access token based on app id and app secret"""
    import json
    import requests
    from preplogger import applogger
    logger = applogger(app)
    #construct request data
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret
    }
    req = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    #print req.text #to test what the FB api responded with
    response_token = req.json()['access_token']

    #data to be stored
    fb_data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "app_access_token": response_token,
    }

    with open(data_location, "w") as fp:
        json.dump(fb_data, fp)
        logger.debug(data_location + " data overwritten with fresh token!")

def fb_ownedpublicapmmetrics(app, pagedata, contextdata, connectiondata):
    """function that retrieves amp data from given msql database"""
    #import msqldb if not loaded yet
    import MySQLdb as mdb
    from preplogger import applogger
    logger = applogger(app)
    #object to return after data is loaded
    apmdata = {
        "page_name": pagedata["name"],
        "page_new_fans": 0,
        "page_new_here": 0,
        "page_new_talks": 0
    }
    querydata ={
        "table": str(connectiondata["page_table"]),
        "start": str(contextdata["yesterday_date"][:10] +" 00:00:00"),
        "end": str(contextdata["yesterday_date"][:10] +" 23:59:59")
    }
    print(querydata)

    #setup connection
    con = mdb.connect(connectiondata["con_ip"], connectiondata["con_user"], connectiondata["con_pass"], connectiondata["con_db"])
    with con:
        cur = con.cursor()
        query = ("SELECT page_name, page_id, page_fan_count, page_were_here_count, page_talking_about_count FROM %(table)s WHERE scrape_date BETWEEN %(start)s AND %(end)s")
        #execute query with context data
        que = cur.execute(query, querydata)
        if que != 0:
            result = cur.fetchall()
            for row in result:
                if row[1] == pagedata["id"]:
                    print(row[0])
                    apmdata["page_new_fans"] = pagedata["fan_count"]-row[2]
                    apmdata["page_new_here"] = pagedata["were_here_count"]-row[3]
                    apmdata["page_new_talks"] = pagedata["talking_about_count"]-row[4]
        cur.close()
        logger.debug(pagedata["name"]+' apm data loaded from mySQL database')
    con.close()
    logger.debug('Connection closed')
    return apmdata


def fb_ownedpubliccomplete(app, pagedata, connectiondata, ipmpostamount):
    """export complete social owned stack page,post and comments"""
    from datetime import datetime
    from datetime import timedelta
    from preplogger import applogger
    from prepdestinations import mysqldestination

    logger = applogger(app)
    #cache general variables
    contextdata = {
        "current_date_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_date": datetime.now(),
        "last_week_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
        "yesterday_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }

    #variables for cumulative calculations
    post_like_total = 0
    post_comment_total = 0
    post_share_total = 0
    post_loop = 0
    #start loop through page posts
    for _ in pagedata["posts"]["data"]:
        #only include pages which creation date is equal to the date 7 days ago (last_week_date)
        if pagedata["posts"]["data"][post_loop]["created_time"][:10] == contextdata["last_week_date"][:10]:
            post_message = ""
            post_comments_count = 0
            post_likes_count = 0
            post_share_count = 0
            if "message" in pagedata["posts"]["data"][post_loop]:
                post_message = pagedata["posts"]["data"][post_loop]["message"]
            if "comments" in pagedata["posts"]["data"][post_loop]:
                post_comments_count = len(pagedata["posts"]["data"][post_loop]["comments"]["data"])
            if "likes" in pagedata["posts"]["data"][post_loop]:
                post_likes_count = len(pagedata["posts"]["data"][post_loop]["likes"]["data"])
            if "shares" in pagedata["posts"]["data"][post_loop]:
                post_share_count = pagedata["posts"]["data"][post_loop]["shares"]["count"]
            #post data to export
            post_obj = {
                "post_table":connectiondata["post_table"],
                "scrape_date": contextdata["current_date_timestamp"],
                "page_id": pagedata["id"],
                "page_name": pagedata["name"],
                "post_id": pagedata["posts"]["data"][post_loop]["id"],
                "post_type": pagedata["posts"]["data"][post_loop]["type"],
                "post_created_time": pagedata["posts"]["data"][post_loop]["created_time"][:-5].replace("T", " "),
                "post_message": post_message.encode('utf8'),
                "post_timeline_visibility": pagedata["posts"]["data"][post_loop]["timeline_visibility"],
                "post_comment_count": post_comments_count,
                "post_like_count": post_likes_count,
                "post_share_count": post_share_count
            }
            #post data insert query
            add_post = ("INSERT INTO %(post_table)s"
                        "(scrape_date, page_id, page_name, post_id, post_type, post_created_time, post_message, post_timeline_visibility, post_comment_count, post_like_count, post_share_count)"
                        "VALUES (%(scrape_date)s, %(page_id)s, %(page_name)s, %(post_id)s, %(post_type)s, %(post_created_time)s, %(post_message)s, %(post_timeline_visibility)s, %(post_comment_count)s, %(post_like_count)s, %(post_share_count)s)")

            #Setup database connection to export post data
            mysqldestination(app, connectiondata, add_post, post_obj)

            #start loop through post comments
            if post_comments_count > 0:
                comment_loop = 0
                #doublecheck if comment key is in post comment json
                if "comments" in pagedata["posts"]["data"][post_loop]:
                    for _ in pagedata["posts"]["data"][post_loop]["comments"]["data"]:
                        #comment data to export
                        post_comment_obj = {
                            "comment_table": connectiondata["comment_table"],
                            "scrape_date": contextdata["current_date_timestamp"],
                            "page_id": pagedata["id"],
                            "post_id": pagedata["posts"]["data"][post_loop]["id"],
                            "comment_id": pagedata["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["id"],
                            "comment_created_time": pagedata["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["created_time"][:-5].replace("T", " "),
                            "comment_message": pagedata["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["message"].encode('utf8'),
                            "comment_like_count": pagedata["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["like_count"],
                            "comment_comment_count": pagedata["posts"]["data"][post_loop]["comments"]["data"][comment_loop]["comment_count"],
                        }
                        #comment data insert query
                        add_comment = ("INSERT INTO %(comment_table)s "
                                       "(scrape_date, page_id, post_id, comment_id, comment_created_time, comment_message, comment_like_count, comment_comment_count)"
                                       "VALUES (%(scrape_date)s, %(page_id)s, %(post_id)s, %(comment_id)s, %(comment_created_time)s, %(comment_message)s, %(comment_like_count)s, %(comment_comment_count)s)")

                        #Setup database connection to export comment data
                        mysqldestination(app, connectiondata, add_comment, post_comment_obj)

                        #increment comment loop
                        comment_loop = comment_loop+1

        #caculate ipm metrics
        post_comments_base = 0
        post_likes_base = 0
        post_share_base = 0
        if "comments" in pagedata["posts"]["data"][post_loop]:
            post_comments_base = len(pagedata["posts"]["data"][post_loop]["comments"]["data"])
        if "likes" in pagedata["posts"]["data"][post_loop]:
            post_likes_base = len(pagedata["posts"]["data"][post_loop]["likes"]["data"])
        if "shares" in pagedata["posts"]["data"][post_loop]:
            post_share_base = pagedata["posts"]["data"][post_loop]["shares"]["count"]

        #aggregate ipm data of last x amount of posts
        if post_loop < ipmpostamount:
            post_like_total = post_like_total + post_comments_base
            post_comment_total = post_comment_total + post_likes_base
            post_share_total = post_share_total + post_share_base
        post_loop = post_loop+1

    #load apm metrics
    apmdata = fb_ownedpublicapmmetrics(app, pagedata, contextdata, connectiondata)
    page_new_fans = apmdata["page_new_fans"]
    page_new_here = apmdata["page_new_here"]
    page_new_talks = apmdata["page_new_talks"]

    #page data to export
    page_obj = {
        "page_table": connectiondata["page_table"],
        "scrape_date": contextdata["current_date_timestamp"],
        "page_id": pagedata["id"],
        "page_name": pagedata["name"],
        "page_fan_count": pagedata["fan_count"],
        "page_were_here_count": pagedata["were_here_count"],
        "page_talking_about_count": pagedata["talking_about_count"],
        "post_like_total": post_like_total,
        "post_comment_total": post_comment_total,
        "post_share_total": post_share_total,
        "page_new_fans": page_new_fans,
        "page_new_here": page_new_here,
        "page_new_talks": page_new_talks
    }
    #page data insert query
    add_pagedata = ("INSERT INTO %(page_table)s "
                    "(scrape_date, page_id, page_name, page_fan_count, page_were_here_count, page_talking_about_count, post_like_total, post_comment_total, post_share_total, page_new_fans, page_new_here, page_new_talks)"
                    "VALUES (%(scrape_date)s, %(page_id)s, %(page_name)s, %(page_fan_count)s, %(page_were_here_count)s, %(page_talking_about_count)s, %(post_like_total)s, %(post_comment_total)s, %(post_share_total)s, %(page_new_fans)s, %(page_new_here)s, %(page_new_talks)s)")

    #Setup database connection to export page data
    mysqldestination(app, connectiondata, add_pagedata, page_obj)
    logger.debug('Page data sent' + pagedata["name"])

def fb_getpageidsmysql(app, connectiondata, querylimit):
    """retrieve an list of all unique ids in facebook owned page table"""
    import MySQLdb as mdb
    from preplogger import applogger
    logger = applogger(app)

    fb_pages = None
    con = mdb.connect(connectiondata["con_ip"],
                      connectiondata["con_user"],
                      connectiondata["con_pass"],
                      connectiondata["con_db"])
    with con:
        cur = con.cursor()
        query = ("SELECT distinct page_id FROM %s LIMIT %s")
        tablepath = connectiondata["db_name"]+"."+connectiondata["page_table"]

        que = cur.execute(query, (tablepath, querylimit))
        result = cur.fetchall()
        fb_pages = result
        cur.close()
    con.close()
    logger.debug('FB Page ids retrieved from '+ connectiondata["page_table"])
    return fb_pages


def fb_getcommentsentimentmsql(app, pageids, connectiondata, sentapidata):
    """get sentiment data from comments in a mysql database"""
    from datetime import datetime
    from datetime import timedelta
    import MySQLdb as mdb
    from preplogger import applogger
    from prepdestinations import mysqldestination
    from prepsentiment import getstringsentiment

    logger = applogger(app)
    #cache general variables
    current_date = datetime.now()
    yesterday_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")


    comment_data_set = None
    con = mdb.connect(connectiondata["con_ip"],
                      connectiondata["con_user"],
                      connectiondata["con_pass"],
                      connectiondata["con_db"])
    with con:
        cur = con.cursor()
        query = ("SELECT scrape_date,page_id,post_id,comment_id,comment_created_time,comment_message,comment_like_count,comment_comment_count FROM fb_comments "
                 "WHERE page_id = %s AND scrape_date BETWEEN %s AND %s")
        query_page_id = pageids[0]
        start = yesterday_date[:10]+" 00:00:00"
        end = yesterday_date[:10]+" 23:59:59"

        que = cur.execute(query, (query_page_id,start, end))

        result = cur.fetchall()
        comment_data_set = result
        cur.close()
    con.close()
    logger.debug('FB unique Page ids retrieved')

    for row in comment_data_set:
        if len(row[5]) > 20:
            request_response = getstringsentiment(app, sentapidata, row[5])
            comment_sentiment_data = {
                "scrape_date": row[0].strftime("%Y-%m-%d %H:%M:%S"),
                "page_id":row[1],
                "post_id":row[2],
                "comment_id":row[3],
                "comment_created_time": row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "comment_message": row[5],
                "comment_like_count":row[6],
                "comment_comment_count":row[7],
                "comment_sent_label": request_response["label"],
                "comment_positivity": request_response["probability"]["pos"],
                "comment_negativity": request_response["probability"]["neg"],
                "comment_neutrality": request_response["probability"]["neutral"]
            }
            add_comment_sentiment = ("INSERT INTO fb_comment_sentiment "
                                     "(scrape_date, page_id, post_id, comment_id, comment_created_time, comment_message, comment_like_count, comment_comment_count,comment_sent_label,comment_positivity,comment_negativity,comment_neutrality)"
                                     "VALUES (%(scrape_date)s, %(page_id)s, %(post_id)s, %(comment_id)s, %(comment_created_time)s, %(comment_message)s, %(comment_like_count)s, %(comment_comment_count)s, %(comment_sent_label)s, %(comment_positivity)s, %(comment_negativity)s, %(comment_neutrality)s)")

            #Setup database connection and send data to mysql
            mysqldestination(app, connectiondata, add_comment_sentiment, comment_sentiment_data)
