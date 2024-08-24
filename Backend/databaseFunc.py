import mysql.connector
import os
import dotenv
dotenv.load_dotenv("../.env")

# Change ../.env file according to pc mysql configuration
MYSQL_USER  = os.environ["MYSQL_USER"]
MYSQL_PASSWORD  = os.environ["MYSQL_PASSWORD"]
DB_HOST  = os.environ["DB_HOST"]
DB_NAME  = os.environ["DB_NAME"]

db = mysql.connector.connect(host=DB_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,database=DB_NAME)
cur = db.cursor()



def getRequests(columnName=True,checkVal=True):
    """
    Returns List of Requests from SQL database where each request is a list of values
    
    -> request list value's order is according to column order in table
    -> You fetch conditional requests by giving value for column name and checkVal for that column

    Args:
        columnName (bool, optional): Column Name of table to check value. Defaults to True.
        checkVal (bool, optional):  Value to be check against . Defaults to True.

    Returns:
        _type_: List of Lists (2D List)
    """
    try:
        cur.execute(f"SELECT * FROM WEBPORTAL WHERE {columnName}={checkVal};")
        requests = cur.fetchall( )
        
    except Exception as e:
        print("[-] Failed to fetch data from Database :",e)
        requests = []
    
    finally:
        return requests

def insertRequest(req):
    """Function to insert request into table

    Args:
        req (list): List of values in order of columns in the table

    Returns:
        _type_: Boolean
        True : If Successfully inserted data
        False: If Failed to insert data with error in console
    """
    try:
        cur.execute(f"INSERT INTO WEBPORTAL VALUES {str(tuple(req))}")
        return True
        
    except Exception as e:
        
        print("[-] Failed to insert request in database :",e)
        return False


def insertManyRequests(requests):
    """
    Function to insert Multiple Requests into the table
    
    Args:
        requests (List): Lists of requests

    Returns:
        _type_: Boolean
        True : If Successfully inserted data
        False: If Failed to insert data with error in console
    """
    
    try:
        for req in requests:
            cur.execute(f"INSERT INTO WEBPORTAL VALUES {str(tuple(req))}")
        return True
    except Exception as e:
        print("[-] Failed to insert request in database : ",e)
        return False
    
 

