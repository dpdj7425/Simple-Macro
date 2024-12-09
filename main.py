# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyautogui
import time
import threading
import keyboard


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(478, 234)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Run 버튼
        self.RunButton = QtWidgets.QPushButton(self.centralwidget)
        self.RunButton.setGeometry(QtCore.QRect(240, 120, 101, 23))
        self.RunButton.setObjectName("RunButton")
        
        # Stop 버튼
        self.StopButton = QtWidgets.QPushButton(self.centralwidget)
        self.StopButton.setGeometry(QtCore.QRect(130, 120, 101, 23))
        self.StopButton.setObjectName("StopButton")
        
        # Exit 버튼
        self.ExitButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(350, 120, 101, 23))
        self.ExitButton.setObjectName("ExitButton")
        
        # x좌표 및 y좌표 입력 필드
        self.xcoor = QtWidgets.QLineEdit(self.centralwidget)
        self.xcoor.setGeometry(QtCore.QRect(240, 20, 113, 20))
        self.xcoor.setObjectName("xcoor")
        self.ycoor = QtWidgets.QLineEdit(self.centralwidget)
        self.ycoor.setGeometry(QtCore.QRect(240, 50, 113, 20))
        self.ycoor.setObjectName("ycoor")
        
        # Save 버튼
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(370, 50, 81, 21))
        self.SaveButton.setObjectName("SaveButton")
        
        # Find 버튼
        self.FindButton = QtWidgets.QPushButton(self.centralwidget)
        self.FindButton.setGeometry(QtCore.QRect(240, 80, 101, 23))
        self.FindButton.setObjectName("FindButton")
        
        # 레이블
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 20, 61, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 50, 61, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 30, 61, 16))
        self.label_3.setObjectName("label_3")
        
        # Delay 입력 필드
        self.delay = QtWidgets.QSpinBox(self.centralwidget)
        self.delay.setGeometry(QtCore.QRect(60, 50, 80, 22))  # 너비를 늘려서 1000까지 입력 가능
        self.delay.setMaximum(1000)  # 최대값 1000으로 설정
        self.delay.setObjectName("delay")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 478, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.ExitButton.clicked.connect(MainWindow.close)  # 프로그램 종료
        self.SaveButton.clicked.connect(self.save_values)  # Save 버튼 클릭 시 save_values 함수 호출
        self.FindButton.clicked.connect(self.start_mouse_position_tracking)  # Find 버튼 클릭 시 마우스 위치 추적 시작
        self.RunButton.clicked.connect(self.start_clicking)  # Run 버튼 클릭 시 클릭 시작
        self.StopButton.clicked.connect(self.stop_clicking)  # Stop 버튼 클릭 시 클릭 중지

        # Ctrl + S, Ctrl + Q, Ctrl + R, Ctrl + F 단축키 설정
        keyboard.add_hotkey('ctrl+s', self.save_values)  # Ctrl + S 키가 눌리면 save_values 호출
        keyboard.add_hotkey('ctrl+q', self.stop_clicking)  # Ctrl + Q 키가 눌리면 stop_clicking 호출
        keyboard.add_hotkey('ctrl+r', self.start_clicking)  # Ctrl + R 키가 눌리면 Run 버튼 클릭
        keyboard.add_hotkey('ctrl+f', self.start_mouse_position_tracking)  # Ctrl + F 키가 눌리면 Find 버튼 클릭

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 상태 플래그
        self.tracking_mouse = False
        self.clicking = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.RunButton.setText(_translate("MainWindow", "Run"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))
        self.FindButton.setText(_translate("MainWindow", "Find"))
        self.label.setText(_translate("MainWindow", "x좌표"))
        self.label_2.setText(_translate("MainWindow", "y좌표"))
        self.label_3.setText(_translate("MainWindow", "Delay"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))  # 제목을 올바르게 설정

    def save_values(self):
        # x좌표, y좌표, delay 값을 변수에 저장
        try:
            self.x = int(self.xcoor.text())
            self.y = int(self.ycoor.text())
            self.delay_time = self.delay.value() / 1000.0  # ms를 초로 변환
            print(f"x좌표: {self.x}, y좌표: {self.y}, Delay: {self.delay_time * 1000} ms")
            self.tracking_mouse = False  # 좌표 저장 후 마우스 위치 추적 중지
        except ValueError:
            print("유효하지 않은 좌표입니다. x좌표와 y좌표를 확인하세요.")

    def start_mouse_position_tracking(self):
        # 마우스 위치 추적 시작
        if not self.tracking_mouse:  # 이미 추적 중이 아닐 때만 시작
            self.tracking_mouse = True
            threading.Thread(target=self.track_mouse_position, daemon=True).start()

    def track_mouse_position(self):
        while self.tracking_mouse:
            x, y = pyautogui.position()  # 현재 마우스 위치 얻기
            self.xcoor.setText(str(x))  # x좌표 입력 필드에 기록
            self.ycoor.setText(str(y))  # y좌표 입력 필드에 기록
            time.sleep(0.001)  # 1ms 대기

    def start_clicking(self):
        # 클릭을 시작하는 스레드 생성
        if not self.clicking:  # 이미 클릭 중이 아닐 때만 시작
            self.clicking = True
            threading.Thread(target=self.click_loop, daemon=True).start()

    def click_loop(self):
        while self.clicking:
            pyautogui.click(self.x, self.y)  # 지정된 좌표 클릭
            time.sleep(self.delay_time)  # delay 시간 대기

    def stop_clicking(self):
        # 클릭 매크로 중지
        self.clicking = False
        print("클릭 매크로가 중지되었습니다.")
        self.activate_main_window()  # 클릭 매크로 중지 후 메인 윈도우 활성화

    def activate_main_window(self):
        # 메인 윈도우를 활성화
        if MainWindow.isHidden():
            MainWindow.show()
        MainWindow.raise_()
        MainWindow.activateWindow()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
