import speedtest
import requests
from datetime import datetime
import mysql.connector
import schedule
import time
import socket

# Create a Speedtest object
speedtester = speedtest.Speedtest()

# Function to get the public IP address
def get_public_ip():
    response = requests.get("https://api.ipify.org")
    ip_address = response.text
    return ip_address

# Function to get the host name
def get_host():
    return socket.gethostname()

# Function to perform the speed test and insert results into MySQL database
def run_speed_test():
    print("Running Speed Test...")
    print("This may take a moment.")

    # Get the best server
    speedtester.get_best_server()

    # Perform the download speed test
    download_speed = speedtester.download() / 1000000

    # Perform the upload speed test
    upload_speed = speedtester.upload() / 1000000

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the public IP address
    ip_address = get_public_ip()

    # Insert results into MySQL database
    insert_speed_test_results(current_datetime, ip_address, download_speed, upload_speed)

    # Display the results
    print("Speed Test Results")
    print(f"IP Address: {ip_address}")
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Date and Time: {current_datetime}")
    print("Speed Test completed.")

def insert_speed_test_results(datetime, ip_address, download_speed, upload_speed):
    connection = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_db",
    )
    cursor = connection.cursor()

    query = "INSERT INTO new_speed (`Date/Time`, `IP Address`, `Download`, `Upload`) VALUES (%s, %s, %s, %s)"
    values = (datetime, ip_address, download_speed, upload_speed)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


# Schedule the speed test to run every 1 minutes
schedule.every(60).minutes.do(run_speed_test)

# Main loop to run the scheduled speed test
while True:
    schedule.run_pending()
    time.sleep(60)
