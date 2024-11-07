import sys
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *

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


class MainScreen(QMainWindow):
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
        self.ui = load_ui("MainWindowFeed.ui", self)
        self.ui.setWindowTitle("Surveillance Feed")
        self.ui.showMaximized()
        # any changes to this window should start with "self.ui"

        #add to dropdown
        self.ui.feed_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        self.ui.feed_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        # set a specific selected value in dropdown
        self.ui.feed_ipselect.setCurrentIndex(1)
         # Print current selection
        current_ipfeed = self.ui.feed_ipselect.currentText()
        print("Currently selected IP location:", current_ipfeed)

        #add to dropdown
        self.ui.remove_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        self.ui.remove_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        self.ui.remove_ipselect.setCurrentIndex(0)
        current_ipremove = self.ui.remove_ipselect.currentText()
        print("Currently selected IP location:", current_ipremove)

        #link function to button
        self.ui.add_btn.clicked.connect(self.cctvsetup_dialog)
        self.ui.remove_btn.clicked.connect(self.open_msg)

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

    def open_msg(self):

        current_ipremove = self.ui.remove_ipselect.currentText()
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
        setupdia_ui = load_ui("SetupCCTV.ui", setupdialog)
        setupdia_ui.setWindowTitle("Setup CCTV")

        # Center the dialog on the screen
        setupdia_ui.setModal(True)
        setupdia_ui.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                setupdia_ui.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )
        #INPUT FIELDS
        #lineEdit_ip = IP ADDRESS
        #lineEdit_usern = USERNAME
        #lineEdit_pass = PASSWORD
        #lineEdit_ccloc = CCTV LOCATION
        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED BELOW THIS LINE

        # Function to close dialog on submit button click
        def close_dialog():
            try:
                setupdia_ui.accept()  # Attempt to close the dialog
            except Exception as e:
                print("Failed to close the dialog:", e)

        setupdia_ui.pbtn_submit.clicked.connect(close_dialog)
        setupdia_ui.error_msg.setText("This is the updated error message.")

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        # Execute the dialog
        setupdia_ui.exec()

    def firedetect_dialog(self):
        firedetecdialog = QDialog(self)
        fdetectdia_ui = load_ui("Fire_Detected.ui", firedetecdialog)
        fdetectdia_ui.setWindowTitle("A Fire has been detected")

        # Center the dialog on the screen
        fdetectdia_ui.setModal(True)
        fdetectdia_ui.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                fdetectdia_ui.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED BELOW THIS LINE

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        fdetectdia_ui.exec()

    def smokedetect_dialog(self):
        smokedetecdialog = QDialog(self)
        sdetectdia_ui = load_ui("Smoke_Detected.ui", smokedetecdialog)
        sdetectdia_ui.setWindowTitle("A Smoke has been detected")

        # Center the dialog on the screen
        sdetectdia_ui.setModal(True)
        sdetectdia_ui.setGeometry(
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
                sdetectdia_ui.accept()  # Attempt to close the dialog
            except Exception as e:
                print("Failed to close the dialog:", e)

        sdetectdia_ui.sd_no.clicked.connect(close_dialog)

        # FUNCTIONS AND CHANGES TO THIS DIALOG MUST BE INSERTED ABOVE THIS LINE

        sdetectdia_ui.exec()










def surveillance():
    app = QApplication(sys.argv)
    win = MainScreen()
    win.show()
    sys.exit(app.exec())

surveillance()
