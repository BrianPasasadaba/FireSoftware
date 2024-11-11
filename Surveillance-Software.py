#main.py

import sys
from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import UI
from Fire_Detection import *


def load_ui(ui_file_name, parent=None):
    ui_file = QFile(ui_file_name)
    if not ui_file.exists():
        print(f"Error: The file '{ui_file_name}' was not found.")
        return None
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    widget = loader.load(ui_file, parent)
    ui_file.close()
    if widget is None:
        print(f"Error: Failed to load '{ui_file_name}'")
    return widget


class MainScreen(QMainWindow,UI.Ui_MainWindow):
# LEFT HEADER ELEMENTS
#feed_ipselect = Dropdown for Main Feed CCTV
#add_btn = Add button for Add CCTV Pop Up Window
#remove_btn = Remove Button for #remove_ipselect dropdown
#remove_ipselect = Dropdown for removing specific CCTV

# RIGHT HEADER ELEMENTS
#header_time = label for time
#header_date = label for date

# MAIN FEED ELEMENTS
#ipinfo_feed1 - ipinfo_feed4 = label
#lb_feed1 - lb_feed4 = label
    def __init__(self):
        super(MainScreen, self).__init__()
        self.setWindowTitle("Surveillance Feed")
        self.setupUi(self)
        self.showMaximized()
        # any changes to this window should start with "self.ui"

        # Initialize detection manager
        self.detection_manager = DetectionManager()
        
        # Start main feed detection
        # self.detection_manager.start_detection(0, self.update_main_feed)

        #add to dropdown
        self.feed_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        self.feed_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        # set a specific selected value in dropdown
        self.feed_ipselect.setCurrentIndex(1)
         # Print current selection
        current_ipfeed = self.feed_ipselect.currentText()
        print("Currently selected IP location:", current_ipfeed)

        #add to dropdown
        self.remove_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        self.remove_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        self.remove_ipselect.setCurrentIndex(0)
        current_ipremove = self.remove_ipselect.currentText()
        print("Currently selected IP location:", current_ipremove)

        #link function to button
        self.add_btn.clicked.connect(self.cctvsetup_dialog)
        self.remove_btn.clicked.connect(self.open_msg)

        # Set up message box
        self.msgbox = QMessageBox(self)
        self.msgbox.setWindowTitle("Warning Message")
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore | QMessageBox.Ok)
        self.msgbox.setDefaultButton(QMessageBox.Ok)
        self.msgbox.setInformativeText("Lorem ipsum Fire Surveillance System")
        # QMessageBox.Ok
        # QMessageBox.Open
        # QMessageBox.Save
        # QMessageBox.Cancel
        # QMessageBox.Close
        # QMessageBox.Yes
        # QMessageBox.No
        # QMessageBox.Abort
        # QMessageBox.Retry
        # QMessageBox.Ignore

    def update_main_feed(self, image):
        """Updates the main feed display, resizing to fit label dimensions"""
        # Get the label dimensions
        label_width = self.lb_feed1.width()
        label_height = self.lb_feed1.height()

        # Scale the image to fit label dimensions
        scaled_image = image.scaled(label_width, label_height, Qt.KeepAspectRatio)

        # Update the label with the scaled image
        self.lb_feed1.setPixmap(QPixmap.fromImage(scaled_image))
        self.lb_feed1.setScaledContents(True)

    def change_main_feed(self, index):
        """Changes the main feed camera"""
        # Stop current detection
        self.detection_manager.stop_detection(0)
        
        # Start detection with new camera
        # You'll need to map dropdown index to camera ID
        camera_id = index  # Replace with actual camera ID mapping
        self.detection_manager.start_detection(camera_id, self.update_main_feed)

    def add_new_cctv_feed(self, cctv_info):
        """Adds a new CCTV feed to the sub-feeds"""
        # Update the IP location labels
        self.ipinfo_feed2.setText(cctv_info["location"])
        self.ipinfo_feed3.setText(cctv_info["location"])
        self.ipinfo_feed4.setText(cctv_info["location"])

        # Update the feed labels
        self.lb_feed2.setText(f"FEED {self.feed_count + 1}")
        self.lb_feed3.setText(f"FEED {self.feed_count + 2}")
        self.lb_feed4.setText(f"FEED {self.feed_count + 3}")

        # Start detection for the new feeds
        self.detection_manager.start_detection(self.feed_count + 1, self.update_sub_feed2)
        self.detection_manager.start_detection(self.feed_count + 2, self.update_sub_feed3)
        self.detection_manager.start_detection(self.feed_count + 3, self.update_sub_feed4)

        self.feed_count += 3  # Increment the feed count

    def update_sub_feed2(self, image):
        """Updates the second sub-feed display"""
        pixmap = QPixmap.fromImage(image)
        self.lb_feed2.setPixmap(pixmap)
        self.lb_feed2.setScaledContents(True)

    def update_sub_feed3(self, image):
        """Updates the third sub-feed display"""
        pixmap = QPixmap.fromImage(image)
        self.lb_feed3.setPixmap(pixmap)
        self.lb_feed3.setScaledContents(True)

    def update_sub_feed4(self, image):
        """Updates the fourth sub-feed display"""
        pixmap = QPixmap.fromImage(image)
        self.lb_feed4.setPixmap(pixmap)
        self.lb_feed4.setScaledContents(True)

    def closeEvent(self, event):
        """Clean up resources when closing the application"""
        self.detection_manager.stop_all()
        event.accept()

    def open_msg(self):

        current_ipremove = self.remove_ipselect.currentText()
        self.msgbox.setText(f"Are you sure you want to remove {current_ipremove}?")

        # Calculate the center position for the message box
        msgbox_geometry = self.msgbox.frameGeometry()
        center_point = self.geometry().center()
        msgbox_geometry.moveCenter(center_point)
        self.msgbox.move(msgbox_geometry.topLeft())

        # Display the message box
        self.msgbox.exec()

    def cctvsetup_dialog(self):
        # Create the dialog and load SetupCCTV.ui into it
        setupdialog = QDialog(self)
        setupdia_ui = UI.Ui_Dialog()
        setupdia_ui.setupUi(setupdialog)
        setupdialog.setWindowTitle("Setup CCTV")

        # Center the dialog on the screen
        setupdialog.setModal(True)
        setupdialog.setGeometry(
            QStyle.alignedRect( 
                Qt.LeftToRight,
                Qt.AlignCenter,
                setupdialog.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )
        #INPUT FIELDS
        lineEdit_ip = setupdia_ui.lineEdit_ip
        lineEdit_usern = setupdia_ui.lineEdit_usern
        lineEdit_pass = setupdia_ui.lineEdit_pass
        lineEdit_ccloc = setupdia_ui.lineEdit_ccloc
        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED BELOW THIS LINE

        # Function to close dialog on submit button click
        def close_dialog():
            try:
                # Get the input values from the fields
                ip = lineEdit_ip.text()
                username = lineEdit_usern.text()
                password = lineEdit_pass.text()
                cclocation = lineEdit_ccloc.text()

                # Print or use the values as needed (for now just printing)
                print(f"IP: {ip}, Username: {username}, Password: {password}, CCTV Location: {cclocation}")
                
                # Attempt to close the dialog
                setupdialog.accept()  
            except Exception as e:
                print("Failed to close the dialog:", e)

        setupdia_ui.pbtn_submit.clicked.connect(close_dialog)
        #setupdia_ui.error_msg.setText("This is the updated error message.")

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        # Execute the dialog
        setupdialog.exec()

    def firedetect_dialog(self):
        firedetectdialog = QDialog(self)
        fdetectdia_ui = UI.Ui_FireDialog
        fdetectdia_ui.setupUi(firedetectdialog)
        fdetectdia_ui.setWindowTitle("A Fire has been detected")

        # Center the dialog on the screen
        firedetectdialog.setModal(True)
        firedetectdialog.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                firedetectdialog.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED BELOW THIS LINE

        # Function to close dialog on submit button click
        def close_dialog():
            try:
                firedetectdialog.accept()  # Attempt to close the dialog
            except Exception as e:
                print("Failed to close the dialog:", e)

        firedetectdialog.sd_no.clicked.connect(close_dialog)

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        firedetectdialog.exec()

    def smokedetect_dialog(self):
        smokedetecdialog = QDialog(self)
        sdetectdia_ui = UI.Ui_SmokeDialog
        sdetectdia_ui.setupUi(smokedetecdialog)
        smokedetecdialog.setWindowTitle("A Smoke has been detected")

        # Center the dialog on the screen
        smokedetecdialog.setModal(True)
        smokedetecdialog.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                sdetectdia_ui.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED BELOW THIS LINE

        # Function to close dialog on submit button click
        def close_dialog():
            try:
                smokedetecdialog.accept()  # Attempt to close the dialog
            except Exception as e:
                print("Failed to close the dialog:", e)

        smokedetecdialog.sd_no.clicked.connect(close_dialog)

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        smokedetecdialog.exec()



def surveillance():
    app = QApplication(sys.argv)
    win = MainScreen()
    win.setWindowTitle("Surveillance Feed")
    # win.setGeometry(100, 100, 800, 600)
    win.showMaximized()
    sys.exit(app.exec())

surveillance()
