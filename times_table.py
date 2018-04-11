import operator
import random
import time
import itertools

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *


class QuizQuestion:
    """Represents a single question
    """
    def __init__(self, first_number, second_number, op = operator.mul):
        self.first_number = first_number
        self.second_number = second_number
        self.answer = op(self.first_number, self.second_number)

    def __eq__(self, other):
        return self.answer == other.answer

    def __str__(self):
        return "{} x {} = {}".format(self.first_number, self.second_number, self.answer)

class QuizQuestionList(list):
    """List of QuizQuestions
    """
    def __init__(self, lowest_number, highest_number):
        question_range = range(lowest_number, highest_number + 1)

        for x, y in itertools.combinations(question_range, 2):
            self.append(QuizQuestion(x, y))

    def next_question(self):
        return self.pop(random.randrange(len(self)))

    def new_question(self):
        return self[random.randrange(len(self))]


class App(QMainWindow):
    """Main App
    """
    def __init__(self):
        super().__init__()
        self.title = 'Times Table Quiz'
        self.left = 50
        self.top = 50
        self.width = 480
        self.height = 320
        self.question_list = QuizQuestionList(2, 12)
        self.question = self.question_list.new_question()
        self.player = QMediaPlayer()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)
        menu_bar = QMenuBar()

        label_style = "font-size: 54px"

        self.question_label = QLabel(self)
        self.question_label.setStyleSheet(label_style)
        self.question_label.move(80, 50)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFixedWidth(320)
        self.question_label.setFixedHeight(100)

        label_string = "{} x {}".format(self.question.first_number,
                                        self.question.second_number)
        self.question_label.setText(label_string)

        self.text_input = QLineEdit(self)
        self.text_input.move(185, 200)

        self.text_input.returnPressed.connect(self.on_return_pressed)

        self.setWindowTitle(self.title)
        self.statusBar().showMessage("Please enter your answer")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def next_prompt(self):
        if len(self.question_list):
            self.question = self.question_list.next_question()
            self.question_label.setText("{} x {}"
                                        .format(self.question.first_number,
                                                self.question.second_number))

    def new_prompt(self):
        if len(self.question_list):
            self.question = self.question_list.new_question()
            self.question_label.setText("{} x {}"
                                        .format(self.question.first_number,
                                                self.question.second_number))


    @pyqtSlot()
    def on_return_pressed(self):
        if self.text_input.text() == str(self.question.answer):
            self.question_label.setText("✓")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/Users/will/src/keya/go-me-go-you.m4a")))
            self.player.play()
            QTimer.singleShot(600, self.next_prompt)
            self.statusBar().showMessage("{} to go!"
                                        .format(len(self.question_list)))
        else:
            self.statusBar().showMessage("{} is not correct. Keep going!".format(self.text_input.text()))
            self.question_label.setText("✘")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/Users/will/src/keya/WrongHonk.mp3")))
            self.player.play()
            self.question_label.setStyleSheet("color: black; font-size: 54px")
            QTimer.singleShot(1000, self.new_prompt)

        self.text_input.clear()

        if not len(self.question_list):
            self.statusBar().showMessage("You did it!")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/Users/will/src/keya/VictoryStrut.mp3")))
            self.player.play()
            self.question_label.setText(">:)")
            self.question_list = QuizQuestionList(2, 4)
            self.question = self.question_list.new_question()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
