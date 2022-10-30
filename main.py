import threading
import datetime

import random
from PyQt5.Qt import QColor,QTableWidget, QDialog,QPushButton,QLineEdit,QLabel,QMessageBox,QComboBox,QCheckBox,QFormLayout,QApplication,QDir,QFont,QFontDatabase,Qt,QIcon,QStandardItemModel,QRect,QPixmap
import sys
import os
import logging
from PyQt5 import QtWidgets


from database import get_availablity,update_value,search_user,set_user_game_status,get_in_game_users
from cachetools import cached, TTLCache


import pyqtgraph as pg
APP_AUTHOR = "عزام"
APP_VERSION = "2.0"


global ready_now
global error
global connection_error
ready_now = False
ready = False
connection_error = False
cache = TTLCache(maxsize=100, ttl=86400)
global selected_items
selected_items = []


date = str(datetime.datetime.now().date())
times = str(datetime.datetime.now().time().strftime(f'%H:%M:%S'))
times = f'{times.split(":")[0] + "-" + times.split(":")[1] + "-" + times.split(":")[2]}'


logging.basicConfig(filename=f"logs [{date +' '+ times}].log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




translate_booking_id={"عصا بلياردو":"billiard_cue",
        "عصا بلياردو المساعد":"billiard_helper_cue",
        "كرة الطاولة":"ping_pong_ball",
        "مضرب كرة الطاولة" :"ping_pong_racket",
         "كرة صغيرة" :"small_football",
         "احجار كيرم خشبية" :"kayram_wooden_ring",
        "احجار كيرم بلاستيكية" :"kayram_plastic_rings",
        "شطرنج" :"chess",
        "دومنو" :"dominoes",
         "بته" :"wild_cards",
        "اونو" :"uno",
        "فودر للكيرم" :"kayram_powder",
        "جهاز بلاستيشن" :"ps4_controller",
         "واير USB" :"usb_cables",
        "شريط بلاستيشن" :"ps4_games"}


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

@cached(cache)
def connect_database(item_name1,student_name1,booking_option1,booking_time1):
    global connection_error
    global ready_now

    try:
        from database import add_new

        ready_now = True
        connection_error = False
        logger.debug("T2")

    except Exception as ex:
        logger.debug("Error in database connection")
        connection_error = True
        logger.debug("Error in database connection")

    if ready_now and item_name1 != '' and student_name1 != '' and booking_option1 != '' and booking_time1 != '':
        add_new(table='sale_log', item_name=str(item_name1), price=str(student_name1), sale_type=str(booking_option1), quantity = str(booking_time1))
        logger.debug("Database connected successfully")

def new_booking(student_id,booking_type,booking_details,booking_time,finishing_date,phone_number=None,name=None):
    try:
        from database import add_new_booking
        add_new_booking(table='entertain_booking',user_id=str(student_id),name=str(name),booking_type=str(booking_type),booking_details=str(booking_details),booking_time=str(booking_time),phone_number=str(phone_number),finish_date=str(finishing_date))
        update_availability_plus(data)
    except:
        logger.debug("Error while adding booking to database")


def update_availability_plus(x):
    try:

        available = get_availablity()
        available = dict(available)
        for s in x:
            for i in available:
                if s == i:
                    used = int(available[i][1])
                    avail = int(available[i][2])
                    used +=int(x[s])
                    avail-=int(x[s])
                    if avail < 0:
                        logger.debug(f"available is not enough {avail, used, x[s]}")
                        break
                    else:
                        update_value(s,str(avail),str(used))
                        available = get_availablity()
    except:
        logger.debug("Error while adding available items into database")


def update_availability_minus(user_id):
    try:
        user_data = search_user(user_id)
        logger.debug(user_data)

        available = get_availablity()
        available = dict(available)
        logger.debug(available)
        for i in user_data:
            for j in available:
                if i == j:
                    used = int(available[i][1])
                    avail = int(available[i][2])
                    used -= int(user_data[i])
                    avail += int(user_data[i])
                    if used<0 or int(available[i][0])<avail:
                        logger.debug(f"Used is lower than 0 or avail in larger than total {avail, used, user_data[i]}")
                        break

                    else:
                        update_value(i, str(avail), str(used))
    except:
        logger.debug("Error while getting user_id details")



thread = threading.Thread(target=connect_database,args=['','','',''])
thread.start()
asci = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM.+-*/=][{}()':;?><,~`!@#$%^&*| "





app = QApplication(sys.argv)
dir_ = QDir("Cairo")
_id = QFontDatabase.addApplicationFont("Fonts\Cairo-Bold.ttf")
dir_ = QDir("Cairo-light")
_id = QFontDatabase.addApplicationFont("Fonts\Cairo-Light.ttf")

# creating checkable combo box class
class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))
        global n
        global s
        n = ""
        s = []

    # when any item get pressed
    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)

        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

        # calling method
        self.check_items()

    # method called by check_items
    def item_checked(self, index):

        # getting item at index
        item = self.model().item(index, 0)

        # return true if checked else false
        return item.checkState() == Qt.Checked

    # calling method
    def check_items(self):
        # blank list
        global checkedItems
        checkedItems = []

        # traversing the items
        for i in range(self.count()):

            # if item is checked add it to the list
            if self.item_checked(i):
                checkedItems.append(i)

        # call this method
        self.update_labels(checkedItems)

    def clearing(self):
        global s
        logger.debug("Clearing function")
     

        for i in range(0,14):
            try:
                if self.item_checked(i) and i not in s:
                    s.append(i)
            except:
                logger.debug("Eror")
        logger.debug(f"Selected items = {s}")

        for i in s:
            # call this method
            item = self.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)
            logger.debug(f"{i} Removed")
        s = []
    # method to update the label
    def update_labels(self, item_list):
        global n

        count = 0
        # traversing the list
        for i in item_list:
            # if count value is 0 don't add comma
            if count == 0:
                n += ' % s' % i
            # else value is greater then 0
            # add comma
            else:
                n += ', % s' % i

            # increment count
            count += 1

        logger.debug(s)
            # setting text to combo box
            #self.setItemText(i)

    # flush
    sys.stdout.flush()



class AnotherWindow(QtWidgets.QMainWindow):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QFormLayout()
        self.label = QLabel("Another Window % d" % random.randint(0, 100))
        layout.addWidget(self.label)
        self.setWindowTitle("أحصائيات حجز النادي الترفيهي")

        self.setLayout(layout)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.scale(1, 1)
        from database import get_all_data
        users = []
        ruf_dates = []
        dates = []
        all_data = get_all_data()

        for i in all_data:
            for s in i:

                if s.isdigit():
                    pass
                else:

                    ruf_dates.append(s)

        for g in ruf_dates:
            dates.append(g.split(" ")[0].split("-")[2])

        dates_nodoublecates = list(dict.fromkeys(dates))

        for a in dates_nodoublecates:
            users.append(dates.count(a))
        print(f"Users list: {users}")
        dates_nodoublecates = [int(x) for x in dates_nodoublecates]
        print(f"Days list: {dates_nodoublecates}")

        for i, item in enumerate(dates_nodoublecates):
            try:
                if item - 1 == dates_nodoublecates[i + 1]:

                    print(item, i)
                else:

                    dates_nodoublecates.insert(i + 1, item - 1)
                    users.insert(i + 1, 0)
            except:
                pass

        hour = dates_nodoublecates
        # hour = [100,2,3,4,5,6,7,8,9,10]
        temperature = users
        # hour = users
        # temperature = dates
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("<span style=\"color:blue;font-size:18pt\">Monthly Data for booking</span>")
        self.graphWidget.setLabel('left', "<span style=\"color:red;font-size:20px\">Users per day</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:red;font-size:20px\">Date Days</span>")

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, pen=pen, symbolSize=5, symbolBrush=('b'))


@cached(cache)
class Apps(QDialog):
    global ready
    global ready_now
    global connection_error

    def __init__(self):


        global connection_error
        global layout
        global data
        global btn_info
        current_dir = os.path.dirname(os.path.realpath(__file__))
        QDialog.__init__(self)
        layout = QFormLayout()



        self.i = 0
        data = {}
        self.folder = ""
        self.user_id = QLineEdit()
        self.student_name = QLineEdit()
        self.booking_time = QLineEdit()
        self.save_location = QLineEdit()
        self.type1 = QLineEdit()
        self.type2 = QLineEdit()
        self.type3 = QLineEdit()
        self.type4 = QLineEdit()
        self.type5 = QLineEdit()
        self.type6 = QLineEdit()
        self.type7 = QLineEdit()
        self.type8 = QLineEdit()
        self.type9 = QLineEdit()
        self.type10 = QLineEdit()
        self.type11 = QLineEdit()
        self.type12 = QLineEdit()
        self.type13 = QLineEdit()
        self.type14 = QLineEdit()
        self.type15 = QLineEdit()

        self.booking_option = QComboBox()

        # creating checkable combo box
        self.booking_type = CheckableComboBox()

        self.photo = QLabel(self)
        self.photo.setGeometry(QRect(0, 0, 80, 95))
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.photo.setPixmap(QPixmap("assets\logo.png"))
        self.photo.move(450,0)
        #self.item.addItem(self.item)
        #self.checking = PyQt5.Qt.QTextList()
        #self.book_list = PyQt5.Qt.QListView()
        self.check_box = QCheckBox("View report/ اظهار تقرير")
        self.line = QLabel("The copyrights © for Azzam, Student_ID: 2103100 | MTC Entertainment center ")

        font = QFont("Cairo")
        font1 = QFont("Cairo-light")
        self.btn_download = QPushButton("إدخال")
        btn_info = QPushButton("معلومات", self)


        self.reset_btn = QPushButton("تطبيق التغييرات", self)
        self.reset_btn.move(400,300)
        btn_info.unsetLayoutDirection()



        self.user_id.setPlaceholderText("Student ID| رقم الطالب")
        self.student_name.setPlaceholderText("Student Name|اسم الطالب (اختياري)")
        self.booking_time.setPlaceholderText("Booking Time|المدة(HH:MM)")
        self.type1.setPlaceholderText("عصا بلياردو")
        self.type2.setPlaceholderText("عصا المساعد")
        self.type3.setPlaceholderText("كرة الطاولة")
        self.type4.setPlaceholderText('مضرب كرة الطاولة')
        self.type5.setPlaceholderText('كورة صغيرة')
        self.type6.setPlaceholderText('احجار كيرم خشب')
        self.type7.setPlaceholderText('احجار كيرم بلاستك')
        self.type8.setPlaceholderText('شطرنج')
        self.type9.setPlaceholderText('دومينو')
        self.type10.setPlaceholderText('بته')
        self.type11.setPlaceholderText('اونو')
        self.type12.setPlaceholderText('فودر للطيرم')
        self.type13.setPlaceholderText('جهاز بلاستيشن')
        self.type14.setPlaceholderText('واير USB')
        self.type15.setPlaceholderText('شريط بلاستيشن')


        self.booking_option.setPlaceholderText(" ")
        self.booking_type.setPlaceholderText(" ")

        #combo boxes
        self.booking_option.addItems(["اضافة","انهاء"])
        self.booking_type.addItems(["عصا بلياردو","عصا بلياردو المساعد","كرة الطاولة","مضرب كرة الطاولة","كرة صغيرة",
                                    "احجار كيرم خشبية","احجار كيرم بلاستيكية","شطرنج","دومنو","بته","اونو","فودر للكيرم","جهاز بلاستيشن","واير USB","شريط بلاستيشن"])

        # FONTS
        #self.line.setFont(font)
        self.student_name.setFont(font)
        self.booking_time.setFont(font)
        self.booking_option.setFont(font)
        self.user_id.setFont(font)
        self.btn_download.setFont(font)
        self.reset_btn.setFont(font)
        btn_info.setFont(font1)
        self.booking_type.setFont(font)
        self.type1.setFont(font)
        self.type2.setFont(font)
        self.type3.setFont(font)
        self.type4.setFont(font)
        self.type5.setFont(font)
        self.type6.setFont(font)
        self.type7.setFont(font)
        self.type8.setFont(font)
        self.type9.setFont(font)
        self.type10.setFont(font)
        self.type11.setFont(font)
        self.type12.setFont(font)
        self.type13.setFont(font)
        self.type14.setFont(font)
        self.type15.setFont(font)

        #layout.addWidget(self.playlist)
        layout.addWidget(self.user_id)
        layout.addWidget(self.check_box)
        layout.addWidget(self.student_name)
        layout.addWidget(self.booking_time)
        layout.addWidget(self.booking_option)
        layout.addWidget(self.btn_download)
        layout.addWidget(self.line)
        layout.addWidget(self.booking_type)
        layout.addWidget(self.type1)
        layout.addWidget(self.type2)
        layout.addWidget(self.type3)
        layout.addWidget(self.type4)
        layout.addWidget(self.type5)
        layout.addWidget(self.type6)
        layout.addWidget(self.type7)
        layout.addWidget(self.type8)
        layout.addWidget(self.type9)
        layout.addWidget(self.type10)
        layout.addWidget(self.type11)
        layout.addWidget(self.type12)
        layout.addWidget(self.type13)
        layout.addWidget(self.type14)
        layout.addWidget(self.type15)



        btn_info.setGeometry(20, 380, 20, 20)
        self.check_box.setGeometry(0,0,200,50)
        self.booking_option.currentTextChanged.connect(self.check_formats)
        self.booking_type.currentTextChanged.connect(self.booking_type_function)

        #system settings
        self.setLayout(layout)
        self.setWindowTitle("برنامج MTC-Entertainment")

        self.setFocus()
        #self.setMaximumSize(500,500)
        self.hight = 500
        self.width = 1024
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.hight)
        self.setAutoFillBackground(10)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'assets\icon.ico')))

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)



        layout.removeWidget(self.student_name)
        layout.removeWidget(self.booking_time)
        layout.removeWidget(self.user_id)
        layout.removeWidget(self.btn_download)
        layout.removeWidget(self.booking_type)

        layout.removeWidget(self.type1)
        layout.removeWidget(self.type2)
        layout.removeWidget(self.type3)
        layout.removeWidget(self.type4)
        layout.removeWidget(self.type5)
        layout.removeWidget(self.type6)
        layout.removeWidget(self.type7)
        layout.removeWidget(self.type8)
        layout.removeWidget(self.type9)
        layout.removeWidget(self.type10)
        layout.removeWidget(self.type11)
        layout.removeWidget(self.type12)
        layout.removeWidget(self.type13)
        layout.removeWidget(self.type14)
        layout.removeWidget(self.type15)

        self.student_name.setFixedWidth(200)
        self.student_name.setFixedHeight(45)
        self.student_name.setAlignment(Qt.AlignRight)
        self.student_name.move(20, 190)


        self.type1.setFixedWidth(100)
        self.type1.setFixedHeight(45)
        self.type1.setAlignment(Qt.AlignRight)


        self.type2.setFixedWidth(100)
        self.type2.setFixedHeight(45)
        self.type2.setAlignment(Qt.AlignRight)


        self.type3.setFixedWidth(100)
        self.type3.setFixedHeight(45)
        self.type3.setAlignment(Qt.AlignRight)


        self.type4.setFixedWidth(100)
        self.type4.setFixedHeight(45)
        self.type4.setAlignment(Qt.AlignRight)

        self.type5.setFixedWidth(100)
        self.type5.setFixedHeight(45)
        self.type5.setAlignment(Qt.AlignRight)

        self.type6.setFixedWidth(100)
        self.type6.setFixedHeight(45)
        self.type6.setAlignment(Qt.AlignRight)

        self.type7.setFixedWidth(100)
        self.type7.setFixedHeight(45)
        self.type7.setAlignment(Qt.AlignRight)

        self.type8.setFixedWidth(100)
        self.type8.setFixedHeight(45)
        self.type8.setAlignment(Qt.AlignRight)

        self.type9.setFixedWidth(100)
        self.type9.setFixedHeight(45)
        self.type9.setAlignment(Qt.AlignRight)

        self.type10.setFixedWidth(100)
        self.type10.setFixedHeight(45)
        self.type10.setAlignment(Qt.AlignRight)

        self.type11.setFixedWidth(100)
        self.type11.setFixedHeight(45)
        self.type11.setAlignment(Qt.AlignRight)

        self.type12.setFixedWidth(100)
        self.type12.setFixedHeight(45)
        self.type12.setAlignment(Qt.AlignRight)

        self.type13.setFixedWidth(100)
        self.type13.setFixedHeight(45)
        self.type13.setAlignment(Qt.AlignRight)

        self.type14.setFixedWidth(100)
        self.type14.setFixedHeight(45)
        self.type14.setAlignment(Qt.AlignRight)


        self.type15.setFixedWidth(100)
        self.type15.setFixedHeight(45)
        self.type15.setAlignment(Qt.AlignRight)

        #self.type3.move(550, 250)

        self.hide_all()

        self.booking_time.setFixedWidth(200)
        self.booking_time.setFixedHeight(45)
        self.booking_time.setAlignment(Qt.AlignRight)
        self.booking_time.move(20, 130)

        self.user_id.setFixedWidth(200)
        self.user_id.setFixedHeight(45)
        self.user_id.setAlignment(Qt.AlignRight)
        self.user_id.move(20, 70)


        self.booking_option.setFixedWidth(90)
        self.booking_option.setFixedHeight(30)


        self.booking_type.setFixedWidth(120)
        self.booking_type.setFixedHeight(40)
        self.booking_type.move(300,135)

        btn_info.unsetLayoutDirection()
        btn_info.setFixedWidth(45)
        btn_info.setFixedHeight(45)


        self.btn_download.setFixedWidth(400)
        self.btn_download.setFixedHeight(45)
        self.btn_download.move(250,300)
        self.btn_download.unsetLayoutDirection()

        self.btn_download.setDefault(True)


        #hide all this things when start the program

        self.user_id.hide()
        self.hide_all()
        self.student_name.hide()
        self.booking_time.hide()
        self.booking_type.hide()
        self.btn_download.hide()
        self.reset_btn.hide()

        #self.cb.setFixedHeight(35)
        self.btn_download.clicked.connect(self.submit)
        self.reset_btn.clicked.connect(self.apply_search)
        self.check_box.clicked.connect(self.check_box_clicked)
        btn_info.clicked.connect(self.info)

        layout.removeWidget(self.line)
        self.line.setGeometry(50,100,500,100)
        self.line.move(20, 430)
        self.line.show()
        fonts = QFont("Cairo", 9)
        self.line.setFont(fonts)
        btn_info.move(15, 380)

        # Current playing
        font3 = QFont("Cairo",12)
        global playing_number
        playing_number = 0
        playing_users = get_in_game_users()

        for i in playing_users:
            playing_number += 1

        self.current_playing = QLabel(f"المستخدمون قيد اللعب الان: {playing_number}")
        logger.debug(f"Currently playing users is updated: {playing_number}")

        layout.addWidget(self.current_playing)
        layout.removeWidget(self.current_playing)
        self.current_playing.setGeometry(50, 200, 250, 50)
        self.current_playing.move(600, 20)
        self.current_playing.show()
        self.current_playing.setFont(font3)

        logger.debug("Checking for internet connection (Connecting to the Database)")

        self.new_tables()
        self.tables.hide()
        self.playing_users_tables.hide()

        while True:

            if ready_now and not connection_error:
                QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                self.setFocus()
                logger.debug("Database connected successfully")
                break
            if connection_error:
                try:
                    QMessageBox.warning(self, "تحذير", "No internet connection")
                    logger.debug("No internet connection - Checking internet again")

                    connect_database(' ',' ',' ',' ')

                    if not connection_error:
                        QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                        logger.debug("Connection successed after failing")
                        break
                    sys.exit()
                except:
                    QMessageBox.warning(self, "تحذير", "Check your internet connection then click OK")
                    sys.exit()

    def new_tables(self):

        availability = get_availablity()
        availability = dict(availability)
        logger.debug("fffff")
        logger.debug(f"Currently booking status data: {availability}")
        from tables import create_table
        test = []
        for i, item in enumerate(availability):
            test.append([item])
            for s in availability[item]:
                test[i].append(s)
        logger.debug("000000")
        # ["asdf",0,0,0,0]
        global gdata
        gdata = {}
        for i, item in enumerate(test):
            if i == 0:
                gdata.update({"Item Name": item})
            elif i == 1:
                gdata.update({"Total": item})
            elif i == 2:
                gdata.update({"Used": item})
            elif i == 3:
                gdata.update({"Available": item})
            else:
                gdata.update({str(random.randint(0, 1000)): item})
        print(gdata)
        logger.debug("11111")

        self.tables = create_table(data=gdata, height=len(gdata), width=4)
        self.layout().addWidget(self.tables)
        self.layout().removeWidget(self.tables)
        self.tables.unsetLayoutDirection()
        self.tables.move(30, 80)
        self.tables.setFixedWidth(350)
        self.tables.setFixedHeight(310)
        self.tables.show()
        logger.debug("22222")
        # if you don't want to allow in-table editing, either disable the table like:
        self.tables.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tables.resizeColumnsToContents()
        self.tables.resizeRowsToContents()

        playing_users = get_in_game_users()
        print(playing_users)
        logger.debug("2222")
        tests = []
        for i, item in enumerate(playing_users):
            tests.append([item])
            for s in playing_users[item]:
                tests[i].append(s)

        # ["asdf",0,0,0,0]
        global playing_users_for_table
        playing_users_for_table = {}
        for i, item in enumerate(tests):
            playing_users_for_table.update({str(random.randint(0, 1000)): item})
        print(playing_users_for_table)

        self.playing_users_tables = create_table(data=playing_users_for_table, height=len(playing_users_for_table),width=4)
        logger.debug("55555")
        self.playing_users_tables.setHorizontalHeaderLabels(
            ["Student ID", "Student Name", "Booking Info", "Finishing Time"])
        self.playing_users_tables.resizeColumnsToContents()
        logger.debug("66666")
        self.layout().addWidget(self.playing_users_tables)
        self.layout().removeWidget(self.playing_users_tables)
        self.playing_users_tables.unsetLayoutDirection()
        self.playing_users_tables.move(660, 80)
        logger.debug("7777")
        self.playing_users_tables.setFixedWidth(300)
        self.playing_users_tables.setFixedHeight(300)
        self.playing_users_tables.show()

        # if you don't want to allow in-table editing, either disable the table like:
        self.playing_users_tables.setEditTriggers(QTableWidget.NoEditTriggers)
        # create a connection to the double click event
        self.playing_users_tables.itemDoubleClicked.connect(self.cell_double_clicked)

        for i in range(0, len(gdata)):  # change Used table color
            self.tables.item(i, 2).setBackground(QColor(255, 0, 0))

        for w in range(0, len(gdata)):  # available table color
            self.tables.item(w, 3).setBackground(QColor(44, 209, 18))
        logger.debug("888")
        try:
            icon_file = "assets\ibilliard_cue.jpg"
            status_item = self.tables.item(0, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\ibilliard_cue_helper.jpg"
            status_item = self.tables.item(1, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\ping_pong_balls.jpg"
            status_item = self.tables.item(2, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\ping_pong_rackets.jpg"
            status_item = self.tables.item(3, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\small_football.png"
            status_item = self.tables.item(4, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\kayram.jpg"
            status_item = self.tables.item(5, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\kayram.jpg"
            status_item = self.tables.item(6, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\chess.jpg"
            status_item = self.tables.item(7, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\dominios.jpg"
            status_item = self.tables.item(8, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\wild_cards2.jpg"
            status_item = self.tables.item(9, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\iuno.jpg"
            status_item = self.tables.item(10, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\kayram_powder.jpg"
            status_item = self.tables.item(11, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\ps4_controller.jpg"
            status_item = self.tables.item(12, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\cable.jpg"
            status_item = self.tables.item(13, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\game_cover.jpg"
            status_item = self.tables.item(14, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))

            icon_file = "assets\game_cover.jpg"
            status_item = self.tables.item(15, 0)
            status_item.setIcon(QIcon(QPixmap(icon_file)))


        except:
            logger.debug("Error in setting Icons for table")
    def show_all(self):
        self.type1.show()
        self.type2.show()
        self.type3.show()
        self.type4.show()
        self.type5.show()
        self.type6.show()
        self.type7.show()
        self.type8.show()
        self.type9.show()
        self.type10.show()
        self.type11.show()
        self.type12.show()
        self.type13.show()
        self.type14.show()
        self.type15.show()

    def hide_all(self):
        self.type1.hide()
        self.type2.hide()
        self.type3.hide()
        self.type4.hide()
        self.type5.hide()
        self.type6.hide()
        self.type7.hide()
        self.type8.hide()
        self.type9.hide()
        self.type10.hide()
        self.type11.hide()
        self.type12.hide()
        self.type13.hide()
        self.type14.hide()
        self.type15.hide()

    def check_formats(self):
        logger.debug("check_formats has been called")
        if self.booking_option.currentText() == "اضافة":
            logger.debug("Add button has been clicked, widget displayed")

            self.user_id.show()
            self.student_name.show()
            self.booking_time.show()
            self.booking_type.show()
            self.btn_download.show()
            self.reset_btn.hide()
            self.reset_function()
            self.btn_download.setDefault(True)

            
        if self.booking_option.currentText() == "انهاء":
            logger.debug("Finish button has been clicked, widget disappeared")
            self.user_id.show()
            self.hide_all()
            self.student_name.hide()
            self.booking_time.hide()
            self.booking_type.hide()
            self.reset_function()
            self.btn_download.hide()
            self.reset_btn.show()
            self.reset_btn.setDefault(True)



    def booking_type_function(self):
        logger.debug("booking_type_function has been called")
        global selected_items
        global unav
        if not translate_booking_id[self.booking_type.currentText()] in selected_items:
            selected_items.append(translate_booking_id[self.booking_type.currentText()])
            logger.debug(f"Selected items: {selected_items}")


            if translate_booking_id[self.booking_type.currentText()] == 'billiard_cue':
                self.type1.show()
                self.type1.move(900,100)

            if translate_booking_id[self.booking_type.currentText()] == 'billiard_helper_cue':
                self.type2.show()
                self.type2.move(900,150)

            if translate_booking_id[self.booking_type.currentText()] == 'ping_pong_ball':
                self.type3.show()
                self.type3.move(900,200)

            if translate_booking_id[self.booking_type.currentText()] == 'ping_pong_racket':
                self.type4.show()
                self.type4.move(900,250)

            if translate_booking_id[self.booking_type.currentText()] == 'small_football':
                self.type5.show()
                self.type5.move(900,300)

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_wooden_ring':
                self.type6.show()
                self.type6.move(900,350)

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_plastic_rings':
                self.type7.show()
                self.type7.move(900,400)

            if translate_booking_id[self.booking_type.currentText()] == 'chess':
                self.type8.show()
                self.type8.move(900,450)

            if translate_booking_id[self.booking_type.currentText()] == 'dominoes':
                self.type9.show()
                self.type9.move(800,100)

            if translate_booking_id[self.booking_type.currentText()] == 'wild_cards':
                self.type10.show()
                self.type10.move(800,150)

            if translate_booking_id[self.booking_type.currentText()] == 'uno':
                self.type11.show()
                self.type11.move(800,200)

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_powder':
                self.type12.show()
                self.type12.move(800,250)

            if translate_booking_id[self.booking_type.currentText()] == 'ps4_controller':
                self.type13.show()
                self.type13.move(800,300)

            if translate_booking_id[self.booking_type.currentText()] == 'usb_cables':
                self.type14.show()
                self.type14.move(800,350)

            if translate_booking_id[self.booking_type.currentText()] == 'ps4_games':
                self.type15.show()
                self.type15.move(800,400)





        else:
            selected_items.remove(translate_booking_id[self.booking_type.currentText()])
            logger.debug(f"Selected items: {selected_items}")

            if translate_booking_id[self.booking_type.currentText()] == 'billiard_cue':
                self.type1.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'billiard_helper_cue':
                self.type2.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'ping_pong_ball':
                self.type3.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'ping_pong_racket':
                self.type4.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'small_football':
                self.type5.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_wooden_ring':
                self.type6.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_plastic_rings':
                self.type7.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'chess':
                self.type8.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'dominoes':
                self.type9.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'wild_cards':
                self.type10.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'uno':
                self.type11.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'kayram_powder':
                self.type12.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'ps4_controller':
                self.type13.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'usb_cables':
                self.type14.hide()

            if translate_booking_id[self.booking_type.currentText()] == 'ps4_games':
                self.type15.hide()



    def reset_function(self):
        logger.debug("reset_function has been called")
        global selected_items
        global data
        data = {}
        self.booking_type.clearing()
        selected_items = []
        self.hide_all()

        self.user_id.setText(None)
        self.student_name.setText(None)
        self.booking_time.setText(None)
        self.type1.setText(None)
        self.type2.setText(None)
        self.type3.setText(None)
        self.type4.setText(None)
        self.type5.setText(None)
        self.type6.setText(None)
        self.type7.setText(None)
        self.type8.setText(None)
        self.type9.setText(None)
        self.type10.setText(None)
        self.type11.setText(None)
        self.type12.setText(None)
        self.type13.setText(None)
        self.type14.setText(None)
        self.type15.setText(None)
        logger.debug("All data has been reset to default")




    def check_box_clicked(self):
        global btn_info

        self.i += 1

        logger.debug("check_box_clicked has been called")
        self.window1 = AnotherWindow()
        self.send = QPushButton("عرض إحصائية الحجز")

        self.send.setDefault(True)

        layout.addWidget(self.send)

        layout.removeWidget(self.send)


        self.send.move(480, 250)
        self.send.show()
        self.send.clicked.connect(lambda checked: self.show_win(self.window1))
        self.send.setFixedHeight(50)
        self.send.setFixedWidth(100)
        self.send.setFont(QFont("Cairo"))
        self.new_tables()





        if self.i % 2 == 0:
            logger.debug("Check box has been Unchecked")
            self.booking_option.clear()
            self.booking_option.addItems(["اضافة", "انهاء"])
            self.booking_type.addItems(
                ["عصا بلياردو", "عصا بلياردو المساعد", "كرة الطاولة", "مضرب كرة الطاولة", "كرة صغيرة",
                 "احجار كيرم خشبية", "احجار كيرم بلاستيكية", "شطرنج", "دومنو", "بته", "اونو", "فودر للكيرم",
                 "جهاز بلاستيشن", "واير USB", "شريط بلاستيشن"])

            self.booking_option.show()
            btn_info.show()
            logger.debug("All widgets has been shown")


            self.send.hide()

            self.playing_users_tables.hide()
            self.tables.hide()



        if self.i % 2 != 0:
            logger.debug("Check box has been checked")

            self.booking_option.hide()
            self.student_name.hide()
            self.booking_time.hide()
            self.user_id.hide()
            self.btn_download.hide()
            self.reset_btn.hide()
            self.booking_type.hide()
            self.hide_all()
            btn_info.hide()
            logger.debug("All widgets has been hidden")
            font = QFont("Cairo", 8)

            logger.debug("Gathered successfully")
            self.playing_users_tables.show()
            self.tables.show()


    def establish_database(self):
        logger.debug("establish_database has been called")
        '''Create a temp database for selected data'''
        for i in selected_items:
            if i == 'billiard_cue':
                data.update({i:self.type1.text()})

            if i == 'billiard_helper_cue':
                data.update({i:self.type2.text()})

            if i == 'ping_pong_ball':
                data.update({i:self.type3.text()})

            if i == 'ping_pong_racket':
                data.update({i:self.type4.text()})
            if i == 'small_football':
                data.update({i:self.type5.text()})
            if i == 'kayram_wooden_ring':
                data.update({i:self.type6.text()})

            if i == 'kayram_plastic_rings':
                data.update({i:self.type7.text()})

            if i == 'chess':
                data.update({i:self.type8.text()})

            if i == 'dominoes':
                data.update({i:self.type9.text()})

            if i == 'wild_cards':
                data.update({i:self.type10.text()})

            if i == 'uno':
                data.update({i:self.type11.text()})

            if i == 'kayram_powder':
                data.update({i:self.type12.text()})

            if i == 'ps4_controller':
                data.update({i:self.type13.text()})

            if i == 'usb_cables':
                data.update({i:self.type14.text()})

            if i == 'ps4_games':
                data.update({i:self.type15.text()})

        logger.debug(f"Selected data(In dictionary) {data}")



    def cell_double_clicked(self):

        current_row = self.playing_users_tables.currentRow()
        current_column = self.playing_users_tables.currentColumn()
        cell_value = self.playing_users_tables.item(current_row, current_column).text()
        print(cell_value)
        try:
            if cell_value.isdigit():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("تحذير بأنهاء لعب للمستخدم")
                dlg.setText(f"Do you really want to finish User ID's: {cell_value} game?\n هل أنت حقاً متأكد بإنهاء اللعب للطالب هذا؟")
                dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dlg.setIcon(QMessageBox.Question)
                button = dlg.exec()
                if button == QMessageBox.Yes:
                    logger.debug("Pressed Yes, Continuing")
                    try:
                        logger.debug("Registering user as finished....")
                        if type(search_user(cell_value)) == dict:
                            update_availability_minus(cell_value)
                            set_user_game_status(cell_value)
                            QMessageBox.information(self, "معلومات", "تم تسجيل إنهاء اللعب للمستخدم")
                            logger.debug(f"Return (Finished) for user: {cell_value} Has succeed")
                            playing_number = 0
                            playing_users = get_in_game_users()
                            for i in playing_users:
                                playing_number += 1
                            self.current_playing.setText(f"المستخدمون قيد اللعب الان: {playing_number}")

                            logger.debug(f"Currently playing users is updated: {playing_number}")
                        else:
                            QMessageBox.warning(self, "تحذير", "لا توجد بيانات لهذا المستخدم")
                    except:
                        QMessageBox.warning(self, "تحذير", "لا توجد بيانات لهذا المستخدم")

                    print(f"User {cell_value} has been deleted")



                else:
                    logger.debug("Pressed No, Breaking")



        except:
            logger.debug("Error while removing player from table")


    def types(self):
        '''Checking if all types is digits'''
        logger.debug("Checking if all types is digits")
        global digit
        digit = False
        for i in data:
            if data[i].isdigit():
                digit = True
            else:
                digit = False
                break
        return digit


    def apply_search(self):
        logger.debug("apply_search has been called")
        try:
            logger.debug("Registering user as finished....")
            if type(search_user(str(self.user_id.text()))) == dict:
                update_availability_minus(str(self.user_id.text()))
                set_user_game_status(str(self.user_id.text()))
                QMessageBox.information(self, "معلومات", "تم تسجيل إنهاء اللعب للمستخدم")
                logger.debug(f"Return (Finished) for user: {self.user_id.text()} Has succeed")
                playing_number = 0
                playing_users = get_in_game_users()
                for i in playing_users:
                    playing_number += 1
                self.current_playing.setText(f"المستخدمون قيد اللعب الان: {playing_number}")
                logger.debug(f"Currently playing users is updated: {playing_number}")
            else:
                QMessageBox.warning(self, "تحذير", "لا توجد بيانات لهذا المستخدم")
        except:
            QMessageBox.warning(self, "تحذير", "لا توجد بيانات لهذا المستخدم")

    def check_availability(self):
        logger.debug("check_availability has been called")
        logger.debug("Checking if selected data is available")
        avail = dict(get_availablity())
        status = []
        not_avail = {}
        for i in data:
            for f in avail:
                if i == f:
                    if int(data[i]) <= int(avail[i][2]):
                        status.append(True)
                    else:
                        status.append(False)
                        not_avail.update({i: [data[i], avail[i]]})
        if all(status):
            logger.debug("All selected in dict(data) is available")
            return True
        else:
            logger.debug(not_avail,"returned false")
            logger.debug("Some of dict(data) is larger than available")
            return not_avail


    def submit(self):

        global data
        global selected_items
        global playing_number
        logger.debug("Submission button has been clicked")
        global ready
        from add_time import get_finish_date
        user_id = self.user_id.text()
        student_name = self.student_name.text()
        booking_time = self.booking_time.text()

        self.establish_database()
        logger.debug(f"user id: {user_id}")
        logger.debug(f"student name: {student_name}")
        logger.debug(f"booked data: {data}")


        try:
            if ready_now and not connection_error:
                logger.debug("Trying to submit data")

                if user_id == '' or booking_time.count(":")!=1 or booking_time == '' or selected_items == [] or not user_id.isdigit() or not str(booking_time.split(":")[0]).isdigit() or not str(booking_time.split(":")[1]).isdigit() or not self.types():
                    logger.debug("Error in Textbox format")
                    if booking_time.count(":") != 1:
                        QMessageBox.warning(self, "تحذير", "لم تقم بأضافة ':' في خانة الوقت")
                        logger.debug("':' hasn't been added to text box")
                    else:
                        QMessageBox.warning(self, "تحذير", "أحد الحقول خاطئة او فارغة يرجى التأكد منها")
                        logger.debug("Empty textbox or forbidden characters written")

                else:
                    try:
                        if search_user(user_id) == False: # Check if there is no in_game for the user
                            logger.debug(f"User_id: {user_id} is clear, There isn't booking before")
                            if self.check_availability() == True: # Check if there is available items to book
                                book_time = get_finish_date(booking_time)
                                new_booking(student_id=user_id,name=student_name,booking_type=selected_items,booking_details=data,booking_time=booking_time,finishing_date=book_time)
                                QMessageBox.information(self, "معلومات", "تم اضافة المنتج في قاعدة البيانات")
                                logger.debug("Data has been submitted successfully")

                                playing_number = 0
                                playing_users = get_in_game_users()
                                for i in playing_users:
                                    playing_number += 1
                                self.current_playing.setText(f"المستخدمون قيد اللعب الان: {playing_number}")
                                logger.debug(f"Currently playing users is : {playing_number}")

                                self.reset_function()
                                logger.debug("Data has been reset successfully")
                            else:
                                not_avail = self.check_availability()
                                for i in not_avail:

                                    logger.debug(f"Book in {i} is invalid, available: {not_avail[i][1][2]}, booked {not_avail[i][0]}")
                                    #QMessageBox.warning(self,"تحذير","لا يكفي احد الحقول للحجز في المتاح")
                                    QMessageBox.warning(self, "تحذير", f"الحجز في {i} غير صالح, المتوفر هو {not_avail[i][1][2]}")
                                data = {}

                        else:
                            logger.debug(f"{user_id} is already playing right now")
                            QMessageBox.warning(self, "تحذير","هذا المستدخدم يلعب بالفعل")
                    except:
                        logger.debug("Something went wrong while adding to database- main.py")
                        QMessageBox.information(self, "معلومات","حدث خطأ في قاعدة البيانات")
            else:
                try:
                    QMessageBox.warning(self, "تحذير", "No internet connection ")
                    logger.debug("No internet connection - Checking internet again - when click submit")
                    connect_database('', '', '','')
                    if not connection_error:
                        QMessageBox.information(self, "معلومات", "تم الاتصال بقاعدة البيانات")
                        logger.debug("Connection successes after failing")
                except:
                    QMessageBox.warning(self, "تحذير", "Check your internet connection then click OK")

        except Exception as ex:
            QMessageBox.warning(self,"تحذير","حدث خطأ ما يرجى المحاولة من جديد")
            logger.debug("Something went wrong")

    def show_win(self,window):
        try:
            if window.isVisible():
                window.hide()
            else:
                window.show()
        except:
            print("hi")

    def info(self,window):

        QMessageBox.information(self,"معلومات عن البرنامج ",f"تم انشاء هذا البرنامج بواسطة {APP_AUTHOR} للكلية العسكرية التقنية\n\n  إصدار البرنامج: {APP_VERSION} \n\n للاستفسار و الابلاغات: 90625671")
        logger.debug("Info button has been clicked")

dialog = Apps()
dialog.show()
app.exec_()
logger.debug("App has been closed")
