# Import necessary modules
import random
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QDesktopWidget
global g_data
global g_list

g_data = {}
g_list = []

# Create app object and execute the app
app = QApplication(sys.argv)

class TableView(QTableWidget):
    def __init__(self, dataw, *args):
        QTableWidget.__init__(self, *args)
        self.dataw = dataw
        self.setData()

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    def setData(self):
        horHeaders = []

        for n, key in enumerate(self.dataw.keys()):

            horHeaders.append(key)
            for m, item in enumerate(self.dataw[key]):
                newitem = QTableWidgetItem(str(item))
                self.setItem(n,m, newitem)
            self.setHorizontalHeaderLabels(horHeaders)

def create_table(height,width,data):
    tables = TableView(data, height, width)
    return tables


#tables = create_table(data=sample_data,height=5,width=len(availability))
#tables.show()

