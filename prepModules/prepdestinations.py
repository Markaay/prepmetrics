"""top docstring.
end of discription.
"""
from prepModules.preplogger import applogger

#destination mySQL
def mysqldestination(app, connectiondata, insertquery, datatoexport):
    """function that sends data to a mysql database.
    end of discription.
    """
    #load mysql if it is not loaded yet
    import MySQLdb as mdb
    logger = applogger(app)
    #setup connection
    con = mdb.connect(connectiondata["con_ip"], connectiondata["con_user"], connectiondata["con_pass"], connectiondata["con_db"])
    with con:
        logger.debug('Connected to mySQL database: '+connectiondata["con_ip"]+' to database: '+connectiondata["con_db"])
        cur = con.cursor()
        cur.execute(insertquery, datatoexport)
        con.commit()
        logger.debug(insertquery+' inserted into mySQL database')
    con.close()
    logger.debug('Connection closed')
