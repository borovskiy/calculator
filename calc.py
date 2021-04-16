from PyQt5 import QtCore, QtGui, QtWidgets

list_button = []
dict_text = {}


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(300, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        for key, value in text_field_customization_dictionary.items():
            text = QtWidgets.QLabel(MainWindow)
            x, y, w, h = value['geometry']
            text.setGeometry(QtCore.QRect(x, y, w, h))
            font = QtGui.QFont()
            font.setPointSize(value['setPointSize'])
            font.setBold(value['setBold'])
            font.setWeight(value['setWeight'])
            text.setFont(font)
            text.setFocusPolicy(QtCore.Qt.NoFocus)
            text.setLayoutDirection(QtCore.Qt.LeftToRight)
            text.setStyleSheet(value['setStyleSheet'])
            text.setText(value['setText'])
            text.setTextFormat(QtCore.Qt.MarkdownText)
            text.setObjectName(value['setObjectName'])
            dict_text.update({value['setObjectName']: text})
        for key, value in dict_button.items():
            x, y, w, h = value[1]
            button = QtWidgets.QPushButton(MainWindow)
            button.setGeometry(QtCore.QRect(x, y, w, h))
            button.setObjectName(key)
            list_button.append([button, value[0]])
        self.retranslateUi(MainWindow)
        self.add_element()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Калькулятор"))
        for button in list_button:
            button[0].setText(_translate("MainWindow", button[1]))

    def add_element(self):
        for value in list_button:
            button = value[0]
            text = value[1]
            button.clicked.connect(lambda state, arg=text: self.write_number(arg))

    def translation_into_number(self, number):
        if '.' in number:
            return float(number)
        return int(number)



    def check_point_in_finish_string(self):
        if len(self.text_enter.text()) > 0:
            value_text_enter = self.text_enter.text()[-1]
            if value_text_enter == '.':
                self.text_enter_2.setText(self.text_enter.text() + '0')
                self.text_enter.setText('')
            else:
                self.text_enter_2.setText(self.text_enter.text())
                self.text_enter.setText('')

    def write_number(self, number):
        self.text_operation = dict_text['text_operation']
        self.text_enter = dict_text['text_enter']
        self.text_enter_2 = dict_text['text_enter_2']
        if number.isdigit():
            if self.text_enter.text() == '0':
                self.text_enter.setText(number)
            else:
                self.text_enter.setText(self.text_enter.text() + number)
        elif number.isdigit() is False:
            if number == '.':
                if len(self.text_enter.text()) > 0:
                    self.text_enter.setText(self.text_enter.text() + number)
            elif number in ('+', '-', '/', '*'):
                self.check_point_in_finish_string()
                self.text_operation.setText(number)
            elif number == '=':
                if self.text_enter.text() and len(self.text_operation.text()) and self.text_enter_2.text():
                    total = eval(
                        f'{self.text_enter_2.text()} {self.text_operation.text()} {self.text_enter.text()}')
                    self.text_enter.setText(f'{total}')
                    self.text_enter_2.setText('')
                    self.text_operation.setText('')
                else:
                    print('Недостаточно аргументов')
            elif number == '+/-':
                if self.text_enter.text()[0] is not '-':
                    self.text_enter.setText('-' + self.text_enter.text())
                elif self.text_enter.text()[0] is '-':
                    self.text_enter.setText(self.text_enter.text().replace('-', ''))
            elif number in ('sin', 'cos'):
                import math
                self.check_point_in_finish_string()
                if number == 'sin':
                    translation_num = self.translation_into_number(self.text_enter_2.text())
                    sin = math.sin(translation_num)
                    self.text_enter.setText(f'{round(sin, 5)}')
                    self.text_enter_2.setText(f'')
                else:
                    translation_num = self.translation_into_number(self.text_enter_2.text())
                    cos = math.sin(translation_num)
                    self.text_enter.setText(f'{round(cos, 5)}')
                    self.text_enter_2.setText(f'')

            elif number == 'C':
                self.text_enter_2.setText('')
                self.text_enter.setText('')
                self.text_operation.setText('')

            elif number == '<-':
                finish_symbol = len(self.text_enter.text()) - 1
                self.text_enter.setText(self.text_enter.text()[0:finish_symbol])

            elif number == 'sq':
                self.check_point_in_finish_string()
                value_int = self.translation_into_number(self.text_enter_2.text())
                self.text_enter.setText(f'{value_int ** 2}')
                self.text_enter_2.setText(f'')


if __name__ == "__main__":
    import sys
    from calculator_fields_settings import dict_button, text_field_customization_dictionary

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
