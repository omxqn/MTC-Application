import threading
from PyQt5.Qt import QDialog,QPushButton,QLineEdit,QLabel,QMessageBox,QComboBox,QCheckBox,QFormLayout,QApplication,QDir,QFont,QFontDatabase,Qt,QIcon,QStandardItemModel,QRect,QPixmap
import sys
import os
import logging
import datetime
from database import get_availablity,update_value,search_user,set_user_game_status,get_in_game_users
from cachetools import cached, TTLCache

APP_AUTHOR = "عزام"
APP_VERSION = "1.2"

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
        self.photo.setPixmap(QPixmap("logo.png"))
        self.photo.move(450,0)
        #self.item.addItem(self.item)
        #self.checking = PyQt5.Qt.QTextList()
        #self.book_list = PyQt5.Qt.QListView()
        self.check_box = QCheckBox("View report/ اظهار تقرير")
        self.line = QLabel("The copyrights © for Azzam, Student_ID: 2103100 | MTC Entertainment center ")

        font = QFont("Cairo")
        font1 = QFont("Cairo-light")
        self.btn_download = QPushButton("إدخال المنتج")
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



        btn_info.setGeometry(10, 280, 10, 10)
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
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'icon.ico')))

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
        btn_info.move(15, 385)

        # Current playing
        font3 =QFont("Cairo",12)
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




    def user_info_function(self):
        user_id = self.get_user_data.text()
        logger.debug("user_info_function has been called")
        try:
            if user_id!= "":

                playing_users = get_in_game_users(user_id)
                logger.debug(f"Gathered information: {playing_users}")
            else:
                playing_users = get_in_game_users()
                logger.debug(f"Gathered information (All playing users): {playing_users}")

            if playing_users == {}:
                QMessageBox.information(self, "تحذير", "لا توجد بيانات لعب عن هذا المستخدم")

            for i in playing_users:
                QMessageBox.information(self,"الّاعبون قيد اللعب",f"User ID: {i}\nName:{playing_users[i][0]}\nBooked Items: {playing_users[i][1]}\nFinishing Time: {playing_users[i][2]}")
                logger.debug(
                    f"User ID: {i}\nName:{playing_users[i][0]}\nBooked Items: {playing_users[i][1]}\nFinishing Time: {playing_users[i][2]}")
        except:
            QMessageBox.information(self,"تحذير","لا توجد بيانات لعب عن هذا المستخدم")

    def check_box_clicked(self):
        global btn_info
        self.i += 1

        logger.debug("check_box_clicked has been called")
        self.get_user_data = QLineEdit()
        self.send = QPushButton("بحث عن المستخدم")
        self.get_user_data.setPlaceholderText("الرقم الجامعي (اختياري)")
        self.send.setDefault(True)

        layout.addWidget(self.get_user_data)
        layout.addWidget(self.send)
        layout.removeWidget(self.get_user_data)
        layout.removeWidget(self.send)

        self.get_user_data.move(515,200)
        self.get_user_data.show()
        self.get_user_data.setFixedHeight(40)
        self.get_user_data.setFixedWidth(130)

        self.send.move(530, 300)
        self.send.show()
        self.send.clicked.connect(self.user_info_function)
        self.send.setFixedHeight(50)
        self.send.setFixedWidth(100)

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

            self.billiard_cue.hide()
            self.billiard_helper_cue.hide()
            self.ping_pong_ball.hide()
            self.ping_pong_racket.hide()
            self.small_football.hide()
            self.kayram_wooden_rings.hide()
            self.kayram_plastic_rings.hide()
            self.chess.hide()
            self.dominoes.hide()
            self.wild_cards.hide()
            self.uno.hide()
            self.kayram_powder.hide()
            self.ps4_controller.hide()
            self.usb_cables.hide()
            self.ps4_games.hide()
            self.send.hide()
            self.get_user_data.hide()


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

            availability = get_availablity()
            availability = dict(availability)
            logger.debug(f"Currently booking status data: {availability}")


            self.billiard_cue = QLabel(f"billiard cue || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['billiard_cue'][2]}, مستخدم: {availability['billiard_cue'][1]}")
            self.billiard_helper_cue = QLabel(f"billiard helper cue || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['billiard_helper_cue'][2]}, مستخدم: {availability['billiard_helper_cue'][1]}")
            self.ping_pong_ball = QLabel(f"Ping pong balls || المجموع: {availability['billiard_cue'][0]} متاح: {availability['ping_pong_ball'][2]}, مستخدم: {availability['ping_pong_ball'][1]}")
            self.ping_pong_racket = QLabel(f"Ping pong rackets || المجموع: {availability['billiard_cue'][0]} متاح: {availability['ping_pong_racket'][2]}, مستخدم: {availability['ping_pong_racket'][1]}")
            self.small_football = QLabel(f"Small football || المجموع: {availability['billiard_cue'][0]} متاح: {availability['small_football'][2]}, مستخدم: {availability['small_football'][1]}")
            self.kayram_wooden_rings = QLabel(f"kayram wooden rings || المجموع: {availability['billiard_cue'][0]} متاح: {availability['kayram_wooden_rings'][2]}, مستخدم: {availability['kayram_wooden_rings'][1]}")
            self.kayram_plastic_rings = QLabel(f"kayram plastic rings || المجموع:  {availability['billiard_cue'][0]} متاح: {availability['kayram_plastic_rings'][2]}, مستخدم: {availability['kayram_plastic_rings'][1]}")
            self.chess = QLabel(f"Chess || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['chess'][2]}, مستخدم: {availability['chess'][1]}")
            self.dominoes = QLabel(f"dominoes || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['dominoes'][2]}, مستخدم: {availability['dominoes'][1]}")
            self.wild_cards = QLabel(f"Wild cards || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['wild_cards'][2]}, مستخدم: {availability['wild_cards'][1]}")
            self.uno = QLabel(f"UNO ||المجموع: {availability['billiard_cue'][0]} متاح: {availability['uno'][2]}, مستخدم: {availability['uno'][1]}")
            self.kayram_powder = QLabel(f"Kayram Powder || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['kayram_powder'][2]}, مستخدم: {availability['kayram_powder'][1]}")
            self.ps4_controller = QLabel(f"PS4 Controllers ||المجموع : {availability['billiard_cue'][0]}  متاح: {availability['ps4_controller'][2]}, مستخدم: {availability['ps4_controller'][1]}")
            self.usb_cables = QLabel(f"USB Cables || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['usb_cables'][2]}, مستخدم: {availability['usb_cables'][1]}")
            self.ps4_games = QLabel(f"PS4 Games || المجموع: {availability['billiard_cue'][0]}  متاح: {availability['ps4_games'][2]}, مستخدم: {availability['ps4_games'][1]}")


            layout.addWidget(self.billiard_cue)
            layout.removeWidget(self.billiard_cue)

            layout.addWidget(self.billiard_helper_cue)
            layout.removeWidget(self.billiard_helper_cue)

            layout.addWidget(self.ping_pong_ball)
            layout.removeWidget(self.ping_pong_ball)

            layout.addWidget(self.ping_pong_racket)
            layout.removeWidget(self.ping_pong_racket)

            layout.addWidget(self.small_football)
            layout.removeWidget(self.small_football)

            layout.addWidget(self.kayram_wooden_rings)
            layout.removeWidget(self.kayram_wooden_rings)

            layout.addWidget(self.kayram_plastic_rings)
            layout.removeWidget(self.kayram_plastic_rings)

            layout.addWidget(self.chess)
            layout.removeWidget(self.chess)

            layout.addWidget(self.dominoes)
            layout.removeWidget(self.dominoes)

            layout.addWidget(self.wild_cards)
            layout.removeWidget(self.wild_cards)

            layout.addWidget(self.uno)
            layout.removeWidget(self.uno)

            layout.addWidget(self.kayram_powder)
            layout.removeWidget(self.kayram_powder)

            layout.addWidget(self.ps4_controller)
            layout.removeWidget(self.ps4_controller)

            layout.addWidget(self.kayram_powder)
            layout.removeWidget(self.kayram_powder)

            layout.addWidget(self.usb_cables)
            layout.removeWidget(self.usb_cables)

            layout.addWidget(self.ps4_games)
            layout.removeWidget(self.ps4_games)

            self.billiard_cue.setGeometry(0, 0, 280, 100)
            self.billiard_cue.move(50,10)
            self.billiard_cue.show()
            self.billiard_cue.setFont(font)

            self.billiard_helper_cue.setGeometry(0, 0, 280, 100)
            self.billiard_helper_cue.move(50, 40)
            self.billiard_helper_cue.show()
            self.billiard_helper_cue.setFont(font)

            self.ping_pong_ball.setGeometry(50, -140, 280, 100)
            self.ping_pong_ball.move(50, 70)
            self.ping_pong_ball.show()
            self.ping_pong_ball.setFont(font)

            self.ping_pong_racket.setGeometry(50,200,280,100)
            self.ping_pong_racket.move(50, 100)
            self.ping_pong_racket.show()
            self.ping_pong_racket.setFont(font)

            self.small_football.setGeometry(50,200,280,100)
            self.small_football.move(50, 130)
            self.small_football.show()
            self.small_football.setFont(font)

            self.kayram_wooden_rings.setGeometry(50,200,280,100)
            self.kayram_wooden_rings.move(50, 160)
            self.kayram_wooden_rings.show()
            self.kayram_wooden_rings.setFont(font)

            self.kayram_plastic_rings.setGeometry(50,200,280,100)
            self.kayram_plastic_rings.move(50, 190)
            self.kayram_plastic_rings.show()
            self.kayram_plastic_rings.setFont(font)

            self.chess.setGeometry(50,200,280,100)
            self.chess.move(50, 220)
            self.chess.show()
            self.chess.setFont(font)

            self.dominoes.setGeometry(50,200,280,100)
            self.dominoes.move(50, 250)
            self.dominoes.show()
            self.dominoes.setFont(font)

            self.wild_cards.setGeometry(50,200,280,100)
            self.wild_cards.move(50, 280)
            self.wild_cards.show()
            self.wild_cards.setFont(font)

            self.uno.setGeometry(50,200,280,100)
            self.uno.move(50, 310)
            self.uno.show()
            self.uno.setFont(font)

            self.kayram_powder.setGeometry(50,200,280,100)
            self.kayram_powder.move(50, 335)
            self.kayram_powder.show()
            self.kayram_powder.setFont(font)

            self.ps4_controller.setGeometry(50,200,280,100)
            self.ps4_controller.move(50, 360)
            self.ps4_controller.show()
            self.ps4_controller.setFont(font)

            self.usb_cables.setGeometry(50,200,280,100)
            self.usb_cables.move(50, 380)
            self.usb_cables.show()
            self.usb_cables.setFont(font)

            self.ps4_games.setGeometry(50,200,280,100)
            self.ps4_games.move(50, 400)
            self.ps4_games.show()
            self.ps4_games.setFont(font)


            logger.debug("Booking status has been displayed")


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

    def info(self):
        QMessageBox.information(self,"معلومات عن البرنامج ",f"تم انشاء هذا البرنامج بواسطة {APP_AUTHOR} للكلية العسكرية التقنية\n\n  إصدار البرنامج: {APP_VERSION} \n\n للاستفسار و الابلاغات: 90625671")
        logger.debug("Info button has been clicked")



dialog = Apps()
dialog.show()
app.exec_()
logger.debug("App has been closed")
