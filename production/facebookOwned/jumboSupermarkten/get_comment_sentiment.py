#dependencies
import urllib2
import json
import requests
from datetime import datetime
from datetime import date
from datetime import timedelta
import MySQLdb as mdb

#Account variables
fb_pages = None

#Database connection info
con_ip = "198.199.126.183"
con_db = "admin_prepmetricsdb"
con_user = "prepper"
con_pass = "VMaiQAKSRP"

#cache general variables
current_date_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now()
last_week_date = (current_date - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
yesterday_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

#get list of ids to loop through
con = mdb.connect(con_ip, con_user, con_pass, con_db)
with con:
    cur = con.cursor()
    query = ("SELECT distinct page_id FROM admin_prepmetricsdb.fb_comments LIMIT 10")

    que = cur.execute(query)
    result = cur.fetchall()
    fb_pages = result
    for row in result:
        print(row) #print(row[0]) = returns only direct string

    cur.close()
con.close()
print(fb_pages)

#get comments for each fb_page of yesterday
for fb_pages_id in fb_pages:
    comment_data_set = None
    con = mdb.connect(con_ip, con_user, con_pass, con_db)
    with con:
        cur = con.cursor()
        query = ("SELECT scrape_date,page_id,post_id,comment_id,comment_created_time,comment_message,comment_like_count,comment_comment_count FROM fb_comments "
        "WHERE page_id = %s AND scrape_date BETWEEN %s AND %s")
        query_page_id = fb_pages_id[0]
        start = yesterday_date[:10]+" 00:00:00"
        end = yesterday_date[:10]+" 23:59:59"

        que = cur.execute(query, (query_page_id,start, end))

        result = cur.fetchall()
        comment_data_set = result
        for row in result:
            print(row)
        cur.close()
    con.close()

    for row in comment_data_set:
        print(row[5])
        if len(row[5]) > 20:
            #post comment for dutch sentiment analysis
            request_headers = {
                "X-Mashape-Key": "GKVSrvHRuDmshiuhXXzV4G4Jssdbp18LtAvjsnWXHa1CyDeyBL",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            request_data = {
                "language": "dutch",
                "text": row[5]
            }
            request = requests.post("https://japerk-text-processing.p.mashape.com/sentiment/", headers = request_headers, data = request_data)
            print(request.json())
            request_response = request.json()
            request_response_label = request_response["label"]

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
            print(comment_sentiment_data)

            add_comment_sentiment = ("INSERT INTO fb_comment_sentiment "
                "(scrape_date, page_id, post_id, comment_id, comment_created_time, comment_message, comment_like_count, comment_comment_count,comment_sent_label,comment_positivity,comment_negativity,comment_neutrality)"
                "VALUES (%(scrape_date)s, %(page_id)s, %(post_id)s, %(comment_id)s, %(comment_created_time)s, %(comment_message)s, %(comment_like_count)s, %(comment_comment_count)s, %(comment_sent_label)s, %(comment_positivity)s, %(comment_negativity)s, %(comment_neutrality)s)")

            #Setup database connection
            con = mdb.connect(con_ip, con_user, con_pass, con_db)
            with con:
                cur = con.cursor()
                cur.execute(add_comment_sentiment, comment_sentiment_data)

                con.commit()

            con.close()