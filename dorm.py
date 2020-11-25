# -*- coding: utf-8 -*-
import sys
import io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')#改变默认输出的标准编码
import pymysql
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QPushButton, QLineEdit, QLabel, QVBoxLayout, QTableWidgetItem
from PyQt5 import QtCore
from Ui_studorm import Ui_MainWindow
import random



#窗口类
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('学生宿舍管理系统')
        #连接数据库
        self.db = pymysql.connect("localhost","root","7043834","studorm" )
        self.cursor = self.db.cursor()
        self.tableWidget_2.setRowCount(100)
    def consult(self):
        stuID  = self.lineEdit.text()
        if stuID == "":
            QMessageBox.critical(self, "错误", "请输入学号", QMessageBox.Yes | QMessageBox.No)  
            return
        self.cursor.execute("SELECT * FROM student WHERE stuID = '%s';" % (stuID))
        record = self.cursor.fetchone()
        print(record)
        
        if record == None:
            QMessageBox.critical(self, "错误", "该学号不存在", QMessageBox.Yes | QMessageBox.No)  
            return
        
        #self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for index in range(5):
            newItem = QTableWidgetItem(str(record[index]))
            print(record[index])
            self.tableWidget.setItem(0, index, newItem)
        

    def showAll(self):
        self.cursor.execute("SELECT * FROM student")
        records = self.cursor.fetchall()
        recordnum = len(records)
        self.label_9.setText(str(recordnum))
        #self.tableWidget_2.setRowCount(recordnum)
        #print("个数为" + self.tableWidget_2.rowCount())
        #self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        for i in range(recordnum):
            for index in range(5):
                newItem = QTableWidgetItem(str(records[i][index]))
                self.tableWidget_2.setItem(i, index, newItem)
    def delete(self):
        stuID = self.lineEdit.text()
        if stuID == "" :
            QMessageBox.critical(self, "错误", "请输入学号", QMessageBox.Yes | QMessageBox.No)  
            print("错误")
            return
        self.cursor.execute("SELECT * FROM student WHERE stuID = %s;" % (stuID))
        record = self.cursor.fetchone()
        if record == None:
            QMessageBox.critical(self, "错误", "该学号不存在", QMessageBox.Yes | QMessageBox.No)  
            print("错误")
            return
        try:
            self.cursor.execute("DELETE FROM student WHERE stuID = '%s';" % (stuID))
            self.db.commit()
        except:
            print("错误")
            self.db.roolback()
    def modify(self):
        print("修改")
        stuID = self.tableWidget.item(0,0).text()
        name = self.tableWidget.item(0,1).text()
        gender = self.tableWidget.item(0,2).text()
        roomNum = self.tableWidget.item(0,3).text()
        phoneNum = self.tableWidget.item(0,4).text()
        if stuID == "" or name == "" or gender == "" or roomNum == "" or phoneNum == "":
            print("错误")
            return
        try:
            self.cursor.execute("UPDATE student SET `name` = '%s', `gender`='%s', `roomNum`='%s', `phoneNum`='%s' WHERE `stuID` = '%s';" %(name, gender, roomNum, phoneNum, stuID))
            self.db.commit()
        except:
            print("错误")
            self.db.roolback()
    def add(self):
        print("添加")
        stuID = self.lineEdit_2.text()
        name = self.lineEdit_3.text()
        gender = self.lineEdit_4.text()
        roomNum = self.lineEdit_5.text()
        phoneNum = self.lineEdit_6.text()    
        if stuID == "" or name == "" or gender == "" or roomNum == "" or phoneNum == "":
            QMessageBox.critical(self, "错误", "请输入完整信息", QMessageBox.Yes | QMessageBox.No)  
            print("错误")
            return
        self.cursor.execute("SELECT * FROM student WHERE stuID = %s;" % (stuID))
        record = self.cursor.fetchone()
        if record != None:
            QMessageBox.critical(self, "错误", "该学号已存在", QMessageBox.Yes | QMessageBox.No)  
            print("错误")
            return
        try:
            self.cursor.execute("INSERT INTO student (stuID, name, gender, roomNum, phoneNum) VALUES ('%s', '%s', '%s', '%s', '%s');" %(stuID, name, gender, roomNum, phoneNum))
            self.db.commit()
        except:
            print("错误")
            self.db.roolback()


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())