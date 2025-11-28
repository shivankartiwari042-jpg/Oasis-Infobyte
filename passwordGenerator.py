import sys
import random
import pyperclip
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QSlider,
    QCheckBox
)
from PyQt6.QtCore import Qt

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Password Generator")
        self.setMinimumWidth(400)

        # Widgets
        self.output = QLineEdit()
        self.output.setReadOnly(True)

        length_label = QLabel("Password Length:")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(4)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)

        self.length_value = QLabel("12")
        self.length_slider.valueChanged.connect(self.update_length)

        self.chk_letters = QCheckBox("Letters")
        self.chk_letters.setChecked(True)
        self.chk_numbers = QCheckBox("Numbers")
        self.chk_numbers.setChecked(True)
        self.chk_symbols = QCheckBox("Symbols")

        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.clicked.connect(self.generate_password)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_password)

        self.status = QLabel("")

        # Layouts
        main = QVBoxLayout()

        length_box = QHBoxLayout()
        length_box.addWidget(length_label)
        length_box.addWidget(self.length_slider)
        length_box.addWidget(self.length_value)

        type_box = QHBoxLayout()
        type_box.addWidget(self.chk_letters)
        type_box.addWidget(self.chk_numbers)
        type_box.addWidget(self.chk_symbols)

        btn_box = QHBoxLayout()
        btn_box.addWidget(self.generate_btn)
        btn_box.addWidget(self.copy_btn)

        main.addWidget(self.output)
        main.addLayout(length_box)
        main.addLayout(type_box)
        main.addLayout(btn_box)
        main.addWidget(self.status)

        self.setLayout(main)

    def update_length(self):
        self.length_value.setText(str(self.length_slider.value()))

    def generate_password(self):
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        symbols = "!@#$%^&*()_+-={}[]:;<>,.?/"

        choices = ""

        if self.chk_letters.isChecked():
            choices += letters
        if self.chk_numbers.isChecked():
            choices += numbers
        if self.chk_symbols.isChecked():
            choices += symbols

        if not choices:
            self.status.setText("Select at least one character type.")
            return

        length = self.length_slider.value()
        pwd = "".join(random.choice(choices) for _ in range(length))

        self.output.setText(pwd)
        self.status.setText("Password generated successfully.")

    def copy_password(self):
        pwd = self.output.text().strip()
        if not pwd:
            self.status.setText("Generate a password first.")
            return

        pyperclip.copy(pwd)
        self.status.setText("Password copied permanently to clipboard.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())
