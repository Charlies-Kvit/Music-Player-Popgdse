import telebot

from support_interface import Ui_Form
from PyQt5.QtWidgets import QWidget
from validate_email import validate_email


class Support(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Поддержка')
        self.okButton.hide()
        self.messageLabel.hide()
        self.pushButton.clicked.connect(self.run)
        self.okButton.clicked.connect(self.exit)

    def run(self):
        mail = self.mail.text()
        problem = self.informationFromUser.toPlainText()
        try:
            if not bool(mail):
                mail = str(None)
            else:
                flag = Support.check(self, mail)
                if not flag:
                    self.label_2.setText("Такой почты нету!")
                    raise TypeError
            if not bool(problem):
                self.label_3.setText("Опишите проблему!!!")
                raise TypeError
            information = [mail, problem]
            token = '5786906777:AAF4Prtt-Xx8PNw6gXSDx7n6_6nu-SqF6LI'
            bot = telebot.TeleBot(token)
            chat_id = '2083681203'
            bot.send_message(chat_id, ":\n".join(information))
            self.pushButton.hide()
            self.informationFromUser.hide()
            self.mail.hide()
            self.label.hide()
            self.label_2.hide()
            self.label_3.hide()
            self.okButton.show()
            self.messageLabel.show()
        except Exception as error:
            pass
    
    def check(self, mail):
        is_valid = validate_email(mail)
        return is_valid

    def exit(self):
        self.close()
