"""all functions for sending data to destination types"""

#destination mySQL
def mysqldestination(app, connectiondata, insertquery, datatoexport):
    """function that sends data to a mysql database"""
    #load mysql if it is not loaded yet
    import MySQLdb as mdb
    #setup connection
    con = mdb.connect(connectiondata["con_ip"], connectiondata["con_user"], connectiondata["con_pass"], connectiondata["con_db"])
    with con:
        cur = con.cursor()
        cur.execute(insertquery, datatoexport)
        con.commit()
    con.close()
