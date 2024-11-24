#main.py

import sys
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import UI
from Fire_Detection import *


def create_rtsp_url(cctv_info):
    """Creates an RTSP URL from CCTV information"""
    ip = cctv_info["ip"]
    username = cctv_info["username"]
    password = cctv_info["password"]
    # Standard RTSP URL format: rtsp://username:password@ip_address:554/stream
    return f"rtsp://{username}:{password}@{ip}:554/stream1" 

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
        self.feed_count = 0
        self.detection_manager = DetectionManager()
        self.active_feeds = {}

        # Define default labels as class attribute
        self.default_labels = {
            "feed2": "FEED 2",
            "feed3": "FEED 3",
            "feed4": "FEED 4"
        }
        # Start main feed detection
        # self.start_main_feed(default_camera)        

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
        self.msgbox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
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

    def start_main_feed(self, cctv_info):
        """Starts the main feed with RTSP stream"""
        rtsp_url = create_rtsp_url(cctv_info)
        self.detection_manager.start_detection(rtsp_url, self.update_main_feed)
        self.active_feeds["main"] = cctv_info

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
        """Changes the main feed camera using RTSP"""
        # Stop current main feed
        self.detection_manager.stop_detection("main")
        
        # Get selected feed info
        selected_text = self.feed_ipselect.currentText()
        selected_ip = selected_text.split(" - ")[0]
        
        # Find corresponding CCTV info
        for feed_id, info in self.active_feeds.items():
            if info["ip"] == selected_ip:
                rtsp_url = create_rtsp_url(info)
                self.detection_manager.start_detection(rtsp_url, self.update_main_feed)
                self.active_feeds["main"] = info
                break

    def reset_feed(self, ip_location):
        """Resets a CCTV feed to default state"""
        ip = ip_location.split(" - ")[0]
        
        for feed_id, info in list(self.active_feeds.items()):
            if info["ip"] == ip:
                # Stop the current detection
                self.detection_manager.stop_detection(feed_id)
                
                # Remove from selection dropdowns
                index = self.feed_ipselect.findText(ip_location)
                if index >= 0:
                    self.feed_ipselect.removeItem(index)
                index = self.remove_ipselect.findText(ip_location)
                if index >= 0:
                    self.remove_ipselect.removeItem(index)
                
                # Reset feed to default state
                if feed_id in ["feed2", "feed3", "feed4"]:
                    # Reset the label text
                    getattr(self, f"ipinfo_{feed_id}").setText("IP Location")
                    getattr(self, f"lb_{feed_id}").setText(self.default_labels[feed_id])
                    
                    # Create a default QPixmap with background color
                    default_pixmap = QPixmap(640, 360)  # 16:9 aspect ratio
                    default_pixmap.fill(Qt.gray)  # Fill with gray background
                    
                    # Set the default pixmap
                    getattr(self, f"lb_{feed_id}").setPixmap(default_pixmap)
                    
                    # Update active feeds with default values
                    self.active_feeds[feed_id] = self.default_feed.copy()
                    self.active_feeds[feed_id]["location"] = f"Default {feed_id.capitalize()}"
                
                break
        
        # Decrement feed count
        if self.feed_count > 0:
            self.feed_count -= 1

    def add_new_cctv_feed(self, cctv_info):
        """Adds a new CCTV feed to the sub-feeds using RTSP."""
        rtsp_url = create_rtsp_url(cctv_info)
        
        if self.feed_count == 0:
            self.ipinfo_feed2.setText(cctv_info["location"])
            self.lb_feed2.setText("FEED 2")
            self.detection_manager.start_detection(rtsp_url, self.update_sub_feed2)
            self.active_feeds["feed2"] = cctv_info

        elif self.feed_count == 1:
            self.ipinfo_feed3.setText(cctv_info["location"])
            self.lb_feed3.setText("FEED 3")
            self.detection_manager.start_detection(rtsp_url, self.update_sub_feed3)
            self.active_feeds["feed3"] = cctv_info

        elif self.feed_count == 2:
            self.ipinfo_feed4.setText(cctv_info["location"])
            self.lb_feed4.setText("FEED 4")
            self.detection_manager.start_detection(rtsp_url, self.update_sub_feed4)
            self.active_feeds["feed4"] = cctv_info

        self.feed_count += 1
        
        # Add the new feed to the selection dropdowns
        feed_text = f"{cctv_info['ip']} - {cctv_info['location']}"
        self.feed_ipselect.addItem(feed_text)
        self.remove_ipselect.addItem(feed_text)

    def update_sub_feed2(self, image):
        """Updates the second sub-feed display, preserving 16:9 aspect ratio"""

        label_width = self.lb_feed2.width()
        label_height = self.lb_feed2.height()

        # Calculate the height based on the 16:9 aspect ratio
        target_width = label_height * 16 / 9

        # Scale the image to the calculated height, preserving aspect ratio
        scaled_image = image.scaledToWidth(int(target_width))

        # Update the label with the scaled image
        self.lb_feed2.setPixmap(QPixmap.fromImage(scaled_image))


    def update_sub_feed3(self, image):
        """Updates the third sub-feed display"""
        label_width = self.lb_feed3.width()
        label_height = self.lb_feed3.height()

        # Calculate the height based on the 16:9 aspect ratio
        target_width = label_height * 16 / 9

        # Scale the image to the calculated height, preserving aspect ratio
        scaled_image = image.scaledToWidth(int(target_width))

        # Update the label with the scaled image
        self.lb_feed3.setPixmap(QPixmap.fromImage(scaled_image))

    def update_sub_feed4(self, image):
        """Updates the fourth sub-feed display"""
        label_width = self.lb_feed4.width()
        label_height = self.lb_feed4.height()

        # Calculate the height based on the 16:9 aspect ratio
        target_width = label_height * 16 / 9

        # Scale the image to the calculated height, preserving aspect ratio
        scaled_image = image.scaledToWidth(int(target_width))

        # Update the label with the scaled image
        self.lb_feed4.setPixmap(QPixmap.fromImage(scaled_image))

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
        # Handle the message box result
        result = self.msgbox.exec()
        if result == QMessageBox.Ok:
            self.reset_feed(current_ipremove)

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

                # Prepare the data to pass
                cctv_info = {
                    "ip": ip,
                    "username": username,
                    "password": password,
                    "location": cclocation
                }

                # Pass data directly to the MainScreen method
                self.add_new_cctv_feed(cctv_info)

                # Print or use the values as needed (for now just printing)
                print(f"IP: {ip}, Username: {username}, Password: {password}, CCTV Location: {cclocation}")
                
                # Close the dialog
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
