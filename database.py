
# pip install mysql-connector-python
import mysql.connector
import datetime
import logging
global times
global date
from cachetools import cached, TTLCache
cache = TTLCache(maxsize=100, ttl=86400)
global items_id


items_id={"billiard_cue":1,
        "billiard_helper_cue":2,
        "ping_pong_ball":3,
        "ping_pong_racket":4,
         "small_football":5,
        "kayram_wooden_ring":6,
        "kayram_plastic_rings":7,
       "chess":8,
       "dominoes":9,
      "wild_cards":10,
        "uno":11,
       "kayram_powder":12,
       "ps4_controller":13,
        "usb_cables":14,
       "ps4_games":15}



dateing = str(datetime.datetime.now().date())
timesss = str(datetime.datetime.now().time().strftime(f'%H:%M:%S'))
timesss = f'{timesss.split(":")[0] + "-" + timesss.split(":")[1] + "-" + timesss.split(":")[2]}'

logging.basicConfig(filename=f"logs [{dateing +' '+ timesss}].log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cached(cache)
def start():
    global times
    global date
    global db
    global my_curser
    date = datetime.datetime.now().date()
    times = datetime.datetime.now().time().strftime(f'%H:%M:%S')
    """        host='db4free.net',
        user='sojjadah',
        passwd='sojjadah99',
        database='sojjadah')"""
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='test')
    my_curser = db.cursor()
    logger.debug("Database connected successfully")
# Create new table
'''
# view table descriptions
my_curser.execute('DESCRIBE id_list')
for i in my_curser:
    logger.debug(i)
'''



def new_table(table_name, instractions):
    '''Create new table'''
    try:
        # UNSIGNED there is no - or +
        # Example: instractions =  mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)
        my_curser.execute(f'CREATE TABLE {table_name} ({instractions})')
        return "Table has been created successfully"
    except Exception:
        return 'This table is already existed'



def delete_all(table_name):
    '''Delete all table information'''
    my_curser.execute(f'DELETE FROM {table_name}')
    logger.debug("All data has been deleted")




def add_new_booking(table, user_id, booking_type, booking_details, booking_time, finish_date,phone_number="Null", name="Null",status='in_game'):  # Insert new details
    '''Add new data in elements'''
    # table = id_list
    #user_id VARCHAR(300),name VARCHAR(300) ,phone_number VARCHAR(300) ,book_date VARCHAR(300),finish_date
    try:
        my_curser.execute(
            f'INSERT INTO {table} (user_id, status, name, booking_type, booking_detail, booking_time, phone_number, book_date,finish_date) VALUES {(user_id, status, name, booking_type, booking_details, booking_time, phone_number, str(date)+" "+str(times), finish_date )}')
        logger.debug("committing")
        db.commit()
        logger.debug("Data saved successfully in database")
    except Exception:
        logger.debug("Error")




def add_new_available_status(table, item_name, total, used, available):  # Insert new details
    '''Add new data in elements'''
    # table = id_list
    #user_id VARCHAR(300),name VARCHAR(300) ,phone_number VARCHAR(300) ,book_date VARCHAR(300),finish_date
    try:
        my_curser.execute(
            f'INSERT INTO {table} (item_name, total, used, available) VALUES {(item_name, total, used, available)}')
        logger.debug("committing")
        db.commit()
        logger.debug("Data saved successfully in database")
    except Exception:
        logger.debug("Error")



def get_table_info(table, parm=None):
    global my_curser
    '''Get infos of the current table'''
    if parm == None:
        try:
            my_curser.execute(f'SELECT item_name,total,used,available FROM {table}')
            logger.debug("test")
            x = []
            for i in my_curser:
                x.append(i)
            logger.debug("Data imported successfully")
            return x

        except Exception:
            logger.debug("Error while gathering information from database")
    else:
        try:
            my_curser.execute(f'SELECT user_id,name,booking_detail,booking_time,finish_date FROM {table}')
            logger.debug("test")
            x = []
            for i in my_curser:
                x.append(i)
            logger.debug("Data imported successfully")
            return x

        except Exception:
            logger.debug("Error while gathering information from database")
def get_availablity(x=False):
    if x == False:
        base = {}
        data = get_table_info("entertain_quantities")
        for i in data:
            base.update({i[0]:[i[1],i[2],i[3]]})

        return base


def update_value(item_name,avail,used):
    my_curser.execute(f'UPDATE `entertain_quantities` SET `used` = {used}, `available` = {avail} WHERE item_ID = {items_id[item_name]}')
    db.commit()
    logger.debug(f"available status for {item_name} has been updated. used {used}, available {avail}")

def add_new(table, item_name, price, sale_type, quantity):
    pass

def set_user_game_status(user_id):
    my_curser.execute(f'UPDATE `entertain_booking` SET `status` = "finished" WHERE (user_id=%s AND status="in_game") ' % str(user_id))
    db.commit()
    logger.debug(f"User status{user_id}, has been updated to 'finished'")

def fix(x):
    s=x
    val1 = ""
    global counts
    counts = 0
    rounds = 0

    for i in s:

        if i == "'":
            rounds += 1
            counts = 1
        if counts == 1 and rounds % 2 != 0 and i != "'":
            val1 += i
        else:
            continue

    global t
    t = ""
    g = {}
    for i in val1:

        if i.isdigit():
            g.update({t: i})
            t = ""
        else:
            t += i
    print(g)
    return g

def get_in_game_users(user_id=None):
    datas = []
    data = {}
    try:
        if user_id==None:
            print("Gathering information of in game users(No user parameter)-database")
            my_curser.execute(
                f'SELECT user_id,name,booking_detail,finish_date FROM entertain_booking WHERE status="in_game"')
            for i in my_curser:
                datas.append(i)
            for s in datas:
                data.update({s[0]: [s[1], fix(s[2]), s[3]]})
            return data
        else:
            my_curser.execute(
                f'SELECT user_id,name,booking_detail,finish_date FROM entertain_booking WHERE (user_id =%s AND status="in_game")' % user_id)
            print(f"Gathering information of in game users(there is user parameter: {user_id})-database")
            for i in my_curser:
                datas.append(i)
            for s in datas:
                data.update({s[0]: [s[1], fix(s[2]), s[3]]})
            return data

    except:
        print("Error while searching and getting in_game users")



def search_user(user_id):
    try:
        my_curser.execute(f'SELECT status,name,booking_detail,booking_time,finish_date FROM entertain_booking WHERE (user_id =%s AND status="in_game")' % user_id)
        x = []
        for i in my_curser:
            for g in i:
                x.append(g)
        s = x[2]
        return fix(s)
    except:
        return False
def new_booking(student_id,booking_type,booking_details,booking_time,finishing_date,phone_number=None,name=None):
    '''global h
    h = ""
    for i in booking_details:
        h = h + i+","+booking_details[i]+"-"
    logger.debug(h)'''
    add_new_booking(table='entertain_booking',user_id=str(student_id),name=str(name),booking_type=str(booking_type),booking_details=str(booking_details),booking_time=str(booking_time),phone_number=str(phone_number),finish_date=str(finishing_date))
    logger.debug(f"New booking has been added {student_id,booking_type,booking_details,booking_time,finishing_date,name}- Database")





start()
if __name__ == "__main__":
    #print(get_in_game_users())

    #print(search_user("2103100"))
    #while True:
        #name = input("Item name: ")
        #total = input("Total available: ")
        #add_new_available_status(table="entertain_quantities", item_name=name, total=total, used=0, available=total)

        #add_new_available_status(table="entertain_quantities",item_name="billiard_cue",total=50,used=0,available=50)



    #new_table("sale_log",
              #'sale_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),price VARCHAR(50) ,sale_type VARCHAR(50) ,date VARCHAR(150)')
    #new_table("entertain_quantities",'item_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),total VARCHAR(50) ,used VARCHAR(50) ,available VARCHAR(50)')
    #new_table("entertain_booking",'book_ID int PRIMARY KEY AUTO_INCREMENT,user_id VARCHAR(300),status VARCHAR(300),name VARCHAR(300),booking_type VARCHAR(300), booking_detail VARCHAR(700) , booking_time VARCHAR(300),phone_number VARCHAR(300) ,book_date VARCHAR(300),finish_date VARCHAR(300)')



    '''    f = open('database_cache.txt', 'w')
    f.write(str(my_curser))
    f.close()

    #logger.debug(get_table_info('sale_log', False))



    # table_columns('vid') '''
