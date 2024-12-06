#main.py

import sys
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
import UI
from Fire_Detection import *
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import traceback
import tempfile
import requests
import threading
import time

load_dotenv()

url : str = os.getenv("SUPABASE_URL")
key : str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def create_rtsp_url(cctv_info):
    """Creates an RTSP URL from CCTV information"""
    ip = cctv_info["ip"]
    if ip == "0":
        return 0
    username = cctv_info["username"]
    password = cctv_info["password"]
    # Standard RTSP URL format: rtsp://username:password@ip_address:554/stream
    return f"rtsp://{username}:{password}@{ip}:554/stream1" 

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
        #self.feed_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        #self.feed_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        # set a specific selected value in dropdown
        self.feed_ipselect.setCurrentIndex(0)
         # Print current selection
        current_ipfeed = self.feed_ipselect.currentText()
        print("Currently selected IP location:", current_ipfeed)

        # Connect the change feed signal
        self.feed_ipselect.currentIndexChanged.connect(self.change_main_feed)

        #self.detection_manager.start_detection(0, self.update_main_feed, self.firedetect_dialog, self.smokedetect_dialog,feed_id = 'main')

        #add to dropdown
        #self.remove_ipselect.addItem("192.168.100.0 - Purok 2 Orchid Street")
        #self.remove_ipselect.addItem("192.168.100.0 - Purok 3 Orchid Street")
        self.remove_ipselect.setCurrentIndex(0)
        current_ipremove = self.remove_ipselect.currentText()
        print("Currently selected IP location:", current_ipremove)

        #link function to button
        self.add_btn.clicked.connect(self.cctvsetup_dialog)
        self.remove_btn.clicked.connect(self.open_msg)

        # Set up message box
        self.msgbox = QMessageBox(self)
        self.msgbox.setWindowTitle("Remove Camera Feed")
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        self.msgbox.setDefaultButton(QMessageBox.Ok)
        self.msgbox.setInformativeText("This will permanently remove the selected camera feed.")
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

        # Setup a timer to update date and time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Update every 1000 ms (1 second)
        
        # Initial update
        self.update_datetime()
    
    def update_datetime(self):
        # Get current date and time
        current_datetime = QDateTime.currentDateTime()
        
        # Update time label
        time_str = current_datetime.toString("h:mm")
        self.header_time.setText(time_str)
        
        # Update date label
        date_str = current_datetime.toString("MMMM d, yyyy")
        self.header_date.setText(date_str)

    def start_main_feed(self, cctv_info):
        """Starts the main feed with RTSP stream"""
        rtsp_url = create_rtsp_url(cctv_info)
        self.detection_manager.start_detection(rtsp_url, self.update_main_feed, self.firedetect_dialog, self.smokedetect_dialog, feed_id='main')
        self.active_feeds["main"] = cctv_info

    def update_main_feed(self, image):
        """Updates the main feed display"""
        if not isinstance(image, QImage):
            print("Warning: Invalid image format received")
            return
            
        try:
            label_width = self.lb_feed1.width()
            label_height = self.lb_feed1.height()

            scaled_image = image.scaled(label_width, label_height, Qt.KeepAspectRatio)
            self.lb_feed1.setPixmap(QPixmap.fromImage(scaled_image))
            self.lb_feed1.setScaledContents(True)
        except Exception as e:
            print(f"Error updating main feed: {e}")

    def change_main_feed(self, index):
        """
        Changes the main feed camera and handles feed swapping.
        
        Args:
            index (int): Index of the selected feed in the feed_ipselect dropdown
        """
        # Validate index
        if index < 0 or index >= self.feed_ipselect.count():
            print(f"Warning: Invalid feed index {index}")
            return
            
        try:
            selected_text = self.feed_ipselect.currentText()
            if not selected_text:
                print("Warning: No feed selected")
                return
                
            # Parse IP and location
            try:
                selected_ip, selected_location = selected_text.split(" - ", 1)
            except ValueError:
                print(f"Error: Invalid feed format: {selected_text}")
                return
            
            # Find the feed info for the selected IP and location
            target_feed_info = None
            target_feed_id = None
            
            for feed_id, info in self.active_feeds.items():
                if info.get("ip") == selected_ip and info.get("location") == selected_location:
                    target_feed_info = info
                    target_feed_id = feed_id
                    break
            
            if not target_feed_info:
                print(f"Warning: Could not find feed information for {selected_text}")
                return
                
            if target_feed_id == "main":
                # No need to swap if selecting the same feed
                return
                
            # Stop current main feed
            self.detection_manager.stop_detection("main")
            
            # Store the old main feed info
            old_main_feed = self.active_feeds["main"].copy()
            
            # Dynamically get the update method for the target feed
            target_update_method = getattr(self, f"update_sub_feed{target_feed_id[-1]}", None)
            
            # Start new main feed
            new_rtsp_url = create_rtsp_url(target_feed_info)
            self.detection_manager.stop_detection(target_feed_id)  # Stop target feed first
            self.detection_manager.start_detection(new_rtsp_url, self.update_main_feed, self.firedetect_dialog, self.smokedetect_dialog, feed_id='main')
            
            # Swap the feeds
            # Update main feed storage
            self.active_feeds["main"] = target_feed_info.copy()
            
            # Restart the old main feed in the target feed's slot
            old_main_rtsp_url = create_rtsp_url(old_main_feed)
            self.detection_manager.start_detection(old_main_rtsp_url, target_update_method, self.firedetect_dialog, self.smokedetect_dialog, feed_id=target_feed_id)
            
            # Update the active feeds dictionary
            self.active_feeds[target_feed_id] = old_main_feed
            
            # Update location texts
            self.ipinfo_feed1.setText(target_feed_info["location"])
            
            # Update the UI labels for the swapped feed
            try:
                info_label = getattr(self, f"ipinfo_{target_feed_id}")
                if info_label:
                    info_label.setText(old_main_feed["location"])
            except Exception as e:
                print(f"Error updating UI location text: {e}")
                
        except Exception as e:
            print(f"Error in change_main_feed: {e}")

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
        """Adds a new CCTV feed to the system, prioritizing the main feed if empty."""
        rtsp_url = create_rtsp_url(cctv_info)
        feed_text = f"{cctv_info['ip']} - {cctv_info['location']}"

        # Check if main feed exists
        if "main" not in self.active_feeds:
            # Start as main feed
            self.ipinfo_feed1.setText(cctv_info["location"])
            self.detection_manager.start_detection(rtsp_url, self.update_main_feed, self.firedetect_dialog, self.smokedetect_dialog, feed_id='main')
            self.active_feeds["main"] = cctv_info
            
            # Add to selection dropdowns
            self.feed_ipselect.addItem(feed_text)
            self.remove_ipselect.addItem(feed_text)
            return

        # Map feed_count to the corresponding feed
        feed_mapping = {
            1: ("feed2", self.update_sub_feed2, self.ipinfo_feed2),
            2: ("feed3", self.update_sub_feed3, self.ipinfo_feed3),
            3: ("feed4", self.update_sub_feed4, self.ipinfo_feed4),
        }

        if self.feed_count in feed_mapping:
            feed_key, update_method, feed_label = feed_mapping[self.feed_count]
            feed_label.setText(cctv_info["location"])
            self.detection_manager.start_detection(rtsp_url, update_method, self.firedetect_dialog, self.smokedetect_dialog, feed_key)
            self.active_feeds[feed_key] = cctv_info
        else:
            print("Maximum number of feeds reached")
            return

        self.feed_count += 1

        # Add the new feed to the selection dropdowns
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

    def notify_web_app(self, data):
        response = requests.post(
            'https://true-the-fire.onrender.com/api/desktop-notification/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        return response.json()
    
    def upload_and_insert_report(
        self,
        bucket_name: str,
        file_path: str,
        storage_path: str,
        where: str,
        date: str,
        time_detected: str,
        status: str,
    ):
        """
        Upload an image to Supabase storage and insert a report into the tempReports table.

        :param bucket_name: Name of the Supabase storage bucket.
        :param file_path: Local file path of the image to upload.
        :param storage_path: Path within the bucket to save the file.
        :param where: Location of the incident.
        :param date: Date of the incident (YYYY-MM-DD).
        :param time_detected: Time the incident was detected (HH:MM:SS).
        :param status: Status of the incident report.
        """
        # Combine date and time into a full timestamp
        full_timestamp = datetime.strptime(f"{date} {time_detected}", "%Y-%m-%d %H:%M:%S")

        # Upload the image to Supabase Storage
        with open(file_path, "rb") as file:
            file_contents = file.read()
            upload_response = supabase.storage.from_(bucket_name).upload(
                storage_path, 
                file_contents,  # Pass file contents directly
                {"content-type": "image/jpeg"}  # Specify content type if known
            )
            print ("Upload Response", upload_response)

        # Get the public URL of the uploaded image
        public_url_response = supabase.storage.from_(bucket_name).get_public_url(storage_path)
        print ("Public URL Response", public_url_response)

        # Insert the report into the tempReports table
        data = {
            "where": where,
            "date": date,
            "time_detected": full_timestamp.isoformat(),
            "proof": public_url_response,
            "status": status,
        }

        try:
            # Execute the insert and capture the response
            response = supabase.table("FireDetection_tempreports").insert(data).execute()
            print("Insert response:", response)
            
            # Check if data was inserted successfully and get the ID
            if response.data and len(response.data) > 0:
                inserted_id = response.data[0]['id']  # Assuming the first item has the ID
                
                # Notify web app with the new record's ID
                self.notify_web_app({
                    'type': 'new_temp_report',
                    'data': {
                        'id': inserted_id,
                        'type': 'fire_detection_report'
                    }
                })

                # Start periodic image updates
                # You can customize the feed_id if needed
                update_thread = self.periodic_image_update(inserted_id)
            
            return response.data
        except Exception as insert_err:
            print(f"Insert Error: {insert_err}")
            raise

    def capture_current_feed_image(self, feed_id='main'):
        # Mapping of feed IDs to their corresponding label widgets
        feed_label_mapping = {
            'main': self.lb_feed1,
            'feed2': self.lb_feed2,
            'feed3': self.lb_feed3,
            'feed4': self.lb_feed4
        }
        
        # Validate feed_id
        if feed_id not in feed_label_mapping:
            raise ValueError(f"Invalid feed_id: {feed_id}. Must be one of {list(feed_label_mapping.keys())}")
        
        # Get the corresponding label widget
        label_widget = feed_label_mapping[feed_id]
        
        # Get the pixmap from the label
        pixmap = label_widget.pixmap()
        
        if pixmap:
            # Use Windows-compatible temporary directory
            temp_dir = tempfile.gettempdir()
            
            # Create a temporary file path with the feed ID included
            temp_image_filename = f"incident_proof_{feed_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            temp_image_path = os.path.join(temp_dir, temp_image_filename)
            
            # Save the pixmap to the temporary file
            save_result = pixmap.save(temp_image_path)
            
            # Add error checking for save
            if not save_result:
                raise Exception(f"Failed to save image for feed {feed_id}")
            
            # Verify file exists
            if not os.path.exists(temp_image_path):
                raise FileNotFoundError(f"Image file was not created at {temp_image_path}")
            
            print(f"Image saved to: {temp_image_path}")
            return temp_image_path
        
        raise Exception(f"No image available to capture for feed {feed_id}")
    
    def periodic_image_update(self, initial_record_id, original_feed_id='main', total_duration=120, interval=30):
        """
        Periodically update the image for a specific report, dynamically tracking the feed.
        
        :param initial_record_id: ID of the initial report record
        :param original_feed_id: Original feed ID when the report was created
        :param total_duration: Total duration for updates (in seconds)
        :param interval: Time between updates (in seconds)
        """
        def update_thread():
            start_time = time.time()
            update_count = 0
            current_feed_id = original_feed_id
            
            while time.time() - start_time < total_duration:
                try:
                    # Dynamically determine the current feed to capture
                    # This is the key modification - track the current feed for the original feed's location
                    current_feed_id = self.get_current_feed_for_location(original_feed_id)
                    
                    # Capture new image from the current feed
                    new_image_path = self.capture_current_feed_image(current_feed_id)
                    
                    # Upload the new image to the same bucket as the original
                    bucket_name = "FireProof"  # Replace with actual bucket name
                    storage_path = f"fire_incident_{current_feed_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    
                    # Open the file and read contents
                    with open(new_image_path, "rb") as file:
                        file_contents = file.read()
                        upload_response = supabase.storage.from_(bucket_name).upload(
                            storage_path, 
                            file_contents,
                            {"content-type": "image/jpeg"}
                        )
                    
                    # Get the public URL of the uploaded image
                    public_url_response = supabase.storage.from_(bucket_name).get_public_url(storage_path)
                    
                    # Update the existing record with the new image URL
                    try:
                        update_response = supabase.table("FireDetection_tempreports").update({
                            "proof": public_url_response
                        }).eq("id", initial_record_id).execute()
                        
                        # Optional: Add some error checking
                        if not update_response.data:
                            print(f"No data returned from update for record {initial_record_id}")
                    except Exception as update_err:
                        print(f"Error updating record: {update_err}")
                    
                    # Notify web app about the update
                    self.notify_web_app({
                        'type': 'updated_record',
                        'data': {
                            'id': initial_record_id,
                            'type': 'fire_detection_report',
                            'current_feed': current_feed_id
                        }
                    })
                    
                    # Clean up the temporary image file
                    os.remove(new_image_path)
                    
                    # Increment update count and wait for next interval
                    update_count += 1
                    time.sleep(interval)
                
                except Exception as e:
                    print(f"Error in periodic image update: {e}")
                    break
            
            print(f"Periodic updates completed. Total updates: {update_count}")
        
        # Start the update process in a separate thread
        update_thread = threading.Thread(target=update_thread)
        update_thread.start()
        return update_thread

    def get_current_feed_for_location(self, original_feed_id):
        """
        Determine the current feed ID for a given original feed's location.
        
        :param original_feed_id: The original feed ID
        :return: Current feed ID where the original location is displayed
        """
        # Get the original location
        original_location = self.active_feeds.get(original_feed_id, {}).get("location")
        
        # Check all active feeds to find where this location is currently displayed
        for feed_id, feed_info in self.active_feeds.items():
            if feed_info.get("location") == original_location:
                return feed_id
        
        # Fallback to the original feed ID if no match is found
        return original_feed_id

    def firedetect_dialog(self, feed_id):
        firedetectdialog = QDialog(self)
        fdetectdia_ui = UI.Ui_FireDialog()
        fdetectdia_ui.setupUi(firedetectdialog)
        firedetectdialog.setWindowTitle("A Fire has been detected")

        # Define the mapping at the start of the method or use self.feed_location_mapping if it's a class attribute
        feed_location_mapping = {
            'main': self.ipinfo_feed1,
            'feed2': self.ipinfo_feed2,
            'feed3': self.ipinfo_feed3,
            'feed4': self.ipinfo_feed4
        }

        firedetectdialog.setModal(True)
        firedetectdialog.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                firedetectdialog.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )

        # Function to close dialog on submit button click
        def close_dialog(confirmed):
            try:
                if confirmed:
                    # Get current date and time
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"Current Date: {current_date}, Current Time: {current_time}")  # Debug print
                    
                    # Capture current feed image
                    try:
                        current_feed_image_path = self.capture_current_feed_image(feed_id)
                        print(f"Captured image path: {current_feed_image_path}")  # Debug print
                    except Exception as e:
                        print(f"Error in capture_current_feed_image: {e}")
                        traceback.print_exc()  # Print full traceback
                        return
                    
                    # Upload report to Supabase
                    try:
                        self.upload_and_insert_report(
                            bucket_name="FireProof",
                            file_path=current_feed_image_path,
                            storage_path=f"fire_incident_{current_date}_{current_time}.jpg",
                            where=feed_location_mapping.get(feed_id, '').text(),  # Location of main feed
                            date=current_date,
                            time_detected=current_time,
                            status=None
                        )
                        print("Report uploaded successfully")  # Debug print
                    except Exception as e:
                        print(f"Error in upload_and_insert_report: {e}")
                        traceback.print_exc()  # Print full traceback
                        return
                
                # Close the dialog
                firedetectdialog.accept()

            except Exception as e:
                print(f"Unexpected error in close_dialog: {e}")
                traceback.print_exc()  # Print full traceback

        # Update the connections
        fdetectdia_ui.sd_yes.clicked.connect(lambda: close_dialog(True))
        fdetectdia_ui.sd_no.clicked.connect(lambda: close_dialog(False))

        firedetectdialog.exec()

    def smokedetect_dialog(self, feed_id):
        smokedetecdialog = QDialog(self)
        sdetectdia_ui = UI.Ui_SmokeDialog()
        sdetectdia_ui.setupUi(smokedetecdialog)
        smokedetecdialog.setWindowTitle("A Smoke has been detected")

        # Define the mapping at the start of the method or use self.feed_location_mapping if it's a class attribute
        feed_location_mapping = {
            'main': self.ipinfo_feed1,
            'feed2': self.ipinfo_feed2,
            'feed3': self.ipinfo_feed3,
            'feed4': self.ipinfo_feed4
        }

        # Center the dialog on the screen
        smokedetecdialog.setModal(True)
        smokedetecdialog.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                smokedetecdialog.size(),
                QApplication.primaryScreen().availableGeometry()
            )
        )

        # Function to close dialog on submit button click
        def close_dialog(confirmed):
            try:
                if confirmed:
                    # Get current date and time
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"Current Date: {current_date}, Current Time: {current_time}")  # Debug print
                    
                    # Capture current feed image
                    try:
                        current_feed_image_path = self.capture_current_feed_image(feed_id)
                        print(f"Captured image path: {current_feed_image_path}")  # Debug print
                    except Exception as e:
                        print(f"Error in capture_current_feed_image: {e}")
                        traceback.print_exc()  # Print full traceback
                        return
                    
                    # Upload report to Supabase
                    try:
                        self.upload_and_insert_report(
                            bucket_name="FireProof",
                            file_path=current_feed_image_path,
                            storage_path=f"fire_incident_{current_date}_{current_time}.jpg",
                            where=feed_location_mapping.get(feed_id, '').text(),  # Location of main feed
                            date=current_date,
                            time_detected=current_time,
                            status=None
                        )
                        print("Report uploaded successfully")  # Debug print
                    except Exception as e:
                        print(f"Error in upload_and_insert_report: {e}")
                        traceback.print_exc()  # Print full traceback
                        return
                
                # Close the dialog
                smokedetecdialog.accept()

            except Exception as e:
                print(f"Unexpected error in close_dialog: {e}")
                traceback.print_exc()  # Print full traceback

        # Update the connections
        sdetectdia_ui.sd_yes.clicked.connect(lambda: close_dialog(True))
        sdetectdia_ui.sd_no.clicked.connect(lambda: close_dialog(False))

        smokedetecdialog.exec()
    
    



def surveillance():
    app = QApplication(sys.argv)
    win = MainScreen()
    win.setWindowTitle("Surveillance Feed")
    # win.setGeometry(100, 100, 800, 600)
    win.showMaximized()
    sys.exit(app.exec())

surveillance()
