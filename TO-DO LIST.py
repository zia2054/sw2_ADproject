from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox
import sqlite3


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("window")
        MainWindow.resize(500, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.task_input = QtWidgets.QLineEdit(self.centralwidget)
        self.task_input.setGeometry(QtCore.QRect(30, 370, 431, 25))
        self.task_input.setObjectName("task_input")

        self.date_input = QtWidgets.QLineEdit(self.centralwidget)
        self.date_input.setGeometry(QtCore.QRect(30, 410, 201, 25))
        self.date_input.setObjectName("date_input")

        self.memo_input = QtWidgets.QLineEdit(self.centralwidget)
        self.memo_input.setGeometry(QtCore.QRect(30, 450, 431, 33))
        self.memo_input.setObjectName("memo_input")

        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(70, 490, 91, 60))
        self.add_button.setObjectName("add_button")

        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setGeometry(QtCore.QRect(330, 490, 91, 60))
        self.remove_button.setObjectName("remove_button")

        self.todo_list = QtWidgets.QTableWidget(self.centralwidget)
        self.todo_list.setGeometry(QtCore.QRect(30, 30, 431, 311))
        self.todo_list.setObjectName("todo_list")

        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(150, 570, 200, 20))

        self.todo_list.setColumnCount(4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_button.clicked.connect(self.add_task)
        self.remove_button.clicked.connect(self.remove_task)
        self.database()

    def database(self):
        global db, db_cursor, tasks, dates, memoes,  x, rows
        db = sqlite3.connect("tasks.db")
        db_cursor = db.cursor()
        try:
            db_cursor.execute("CREATE TABLE to_do (id INTEGER PRIMARY KEY AUTOINCREMENT,task text,date text,memo text)")
        except:
            pass

        db_cursor.execute("SELECT * FROM to_do")

        self.todo_list.clearContents()
        self.todo_list.setRowCount(0)

        data = db_cursor.fetchall()
        #db에 작성한 할일 추가
        for r1 in range(len(data)):
            item = data[r1]
            item = list(item)
            self.todo_list.insertRow(r1)
            self.todo_list.setItem(r1, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.todo_list.setItem(r1, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.todo_list.setItem(r1, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.todo_list.setItem(r1, 3, QtWidgets.QTableWidgetItem(item[3]))

        self.todo_list.resizeColumnsToContents()
        labels = ["순서", "할 일", "마감일자", "메모"]
        self.todo_list.setHorizontalHeaderLabels(labels)

    def add_task(self):
        new_task = self.task_input.text()
        new_date = self.date_input.text()
        new_memo = self.memo_input.text()
        if len(new_task) == 0 or len(new_date) == 0:
            self.info_label.setText("빠짐없이 작성해 주세요!")
            self.info_label.adjustSize()
            return None
        self.info_label.setText("")
        db_cursor.execute("INSERT INTO to_do(task,date,memo) VALUES (:task,:date,:memo)", {'task': new_task, 'date': new_date, 'memo': new_memo})
        db.commit()
        self.connect_database()

    def remove_task(self):
        selected = self.todo_list.selectedItems()
        for index in selected:
            idx = self.todo_list.item(index.row(), 0)
            idx = idx.text()
            db_cursor.execute(f"DELETE FROM to_do WHERE id = {idx} ")
            db_cursor.execute("delete from sqlite_sequence where name='to_do';")
            db.commit()
            self.todo_list.removeRow(index.row())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("window", "To-Do List"))
        self.task_input.setPlaceholderText(_translate("window", "할 일을 입력하세요!"))
        self.date_input.setPlaceholderText(_translate("window", "마감일자"))
        self.memo_input.setPlaceholderText(_translate("window", "메모(선택)"))
        self.add_button.setText(_translate("window", "Add"))
        self.remove_button.setText(_translate("window", "Remove"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())