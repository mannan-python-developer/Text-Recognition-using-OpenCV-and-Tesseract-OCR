import cv2
import pytesseract
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QStackedWidget, QMessageBox
import mysql.connector
import sys
import icons_rc

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class user_in(QDialog):
    def __init__(self, widget):
        super(user_in, self).__init__()
        loadUi('upload_image.ui', self)
        self.upload_img.clicked.connect(self.uploadfunction)
        self.widget = widget

    def uploadfunction(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Image Files (*.png *.jpg *.bmp)')
        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()[0]

            # Convert the image to grayscale
            image = cv2.imread(filename)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Perform text recognition
            extracted_text = pytesseract.image_to_string(gray_image)

            extract = Extract(filename, extracted_text)
            self.widget.addWidget(extract)
            self.widget.setFixedWidth(1000)
            self.widget.setFixedHeight(560)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class Extract(QDialog):
    def __init__(self, filename, extracted_text):
        super(Extract, self).__init__()
        loadUi('text_recognition.ui', self)

        self.copied_label.setText(" ")
        self.error_label.setText(" ")

        self.extracted_text.setText(extracted_text)
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaled(self.image_box.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.image_box.setPixmap(pixmap)
        self.image_box.setAlignment(QtCore.Qt.AlignCenter)

        self.change_img_btn.clicked.connect(self.change_imgfunction)
        self.copy_text_btn.clicked.connect(self.copy_textfunction)
        self.save_text_btn.clicked.connect(self.save_Databasefunction)

        # For Saving into Database
        self.extracted_text_data = extracted_text
        self.save_img = filename

        try:

            # Firstly Import the database file from Database Folder in MYSQL Workbanch.
            # Then enter your host, Username and Password.
            db_config = {
                'host': 'localhost',
                'user': '',
                'password': '',
                'database': 'text_recognition'
            }

            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor()

            table_query = ("CREATE TABLE IF NOT EXISTS extracted_data ("
                           "id INT AUTO_INCREMENT PRIMARY KEY,"
                           "data DATETIME DEFAULT CURRENT_TIMESTAMP,"
                           "extracted_text TEXT,"
                           "image LONGBLOB"
                           ")")

            self.cursor.execute(table_query)

        except mysql.connector.Error as e:
            print("Error occurred:", e)
            self.error_label.setText("Error occurred: Database can't be created.")

    def change_imgfunction(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Image Files (*.png *.jpg *.bmp)')
        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()[0]

            # Convert the image to grayscale
            image = cv2.imread(filename)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Perform text recognition
            extracted_text = pytesseract.image_to_string(gray_image)

            # For Saving into Database
            self.extracted_text_data = extracted_text
            self.save_img = filename

            self.copied_label.setText(" ")
            self.error_label.setText(" ")

            self.extracted_text.setText(extracted_text)
            pixmap = QPixmap(filename)
            pixmap = pixmap.scaled(self.image_box.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.image_box.setPixmap(pixmap)
            self.image_box.setAlignment(QtCore.Qt.AlignCenter)

    def copy_textfunction(self):

        self.copied_label.setText(" ")
        self.error_label.setText(" ")

        text_to_copy = self.extracted_text.toPlainText()

        # Check if there's any text to copy
        if text_to_copy.strip():
            QApplication.clipboard().setText(text_to_copy)
            self.copied_label.setText("Text has been copied to clipboard.")
        else:
            self.error_label.setText("There is noting to copy.")

    def save_Databasefunction(self):

        self.copied_label.setText(" ")
        self.error_label.setText(" ")

        try:
            img = self.save_img
            extracted_data = self.extracted_text_data

            if extracted_data.strip():
                # Check if the exact text already exists in the table
                self.cursor.execute("SELECT id FROM extracted_data WHERE extracted_text = %s", (extracted_data,))
                existing_row = self.cursor.fetchone()
                if existing_row:
                    existing_id = existing_row[0]
                    # If the text already exists, display an error message
                    QMessageBox.information(self, "Aleardy saved", f"Text already exists in the database (ID# {existing_id}).")
                else:

                    self.cursor.execute("INSERT INTO extracted_data (extracted_text, image) VALUES (%s, %s)",
                                        (extracted_data, img))
                    self.connection.commit()

                    inserted_id = self.cursor.lastrowid
                    self.copied_label.setText(f"Saved Successfully. (ID# {inserted_id})")
            else:
                self.error_label.setText("There is no text for saving.")
        except:
            self.error_label.setText("Error occurred while saving.")


app = QApplication(sys.argv)
widget = QStackedWidget()
window = user_in(widget)
widget.addWidget(window)
widget.setFixedWidth(440)
widget.setFixedHeight(170)

widget.show()
app.exec_()