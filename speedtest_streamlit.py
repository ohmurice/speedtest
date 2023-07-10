import speedtest
import requests
from datetime import datetime
import mysql.connector
import schedule
import streamlit as st
import time

# Create a Speedtest object
speedtester = speedtest.Speedtest()

# Function to get the public IP address
def get_public_ip():
    response = requests.get("https://api.ipify.org")
    ip_address = response.text
    return ip_address

# Function to perform the speed test and insert results into MySQL database
def run_speed_test():
    st.subheader("Running Speed Test...")
    st.write("This may take a moment.")

    # Get the best server
    speedtester.get_best_server()

    # Perform the download speed test
    download_speed = speedtester.download() / 1000

    # Perform the upload speed test
    upload_speed = speedtester.upload() / 1000

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the public IP address
    ip_address = get_public_ip()

    # Insert results into MySQL database
    insert_speed_test_results(current_datetime, ip_address, download_speed, upload_speed)

    # Display the results
    st.subheader("Speed Test Results")
    st.write(f"IP Address: {ip_address}")
    st.write(f"Download Speed: {download_speed:.2f} Kbps")
    st.write(f"Upload Speed: {upload_speed:.2f} Kbps")
    st.write(f"Date and Time: {current_datetime}")

# Function to insert speed test results into MySQL database
def insert_speed_test_results(datetime, ip_address, download_speed, upload_speed):
    connection = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_db",
    )
    cursor = connection.cursor()

    query = "INSERT INTO speed_test (`Date/Time`, `IP Address`, `Download`, `Upload`) VALUES (%s, %s, %s, %s)"
    values = (datetime, ip_address, download_speed, upload_speed)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Schedule the speed test to run every 1 minute
schedule.every(1).minutes.do(run_speed_test)

# Main app
def main():
    # Custom CSS styles
    st.markdown(
        """
        <style>
        body {
            background-color: #F5F8FA;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .header-container {
            background-color: #1DA1F2;
            padding: 1rem;
            color: white;
            margin-bottom: 1rem;
        }
        .content-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .speed-results {
            margin-top: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App header
    st.container().markdown(
        """
        <div class="header-container">
            <h1>Internet Speed Test</h1>
            <p>Test your internet connection speed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Run the speed test when the program is open
    #if st.open("Run Speed Test"):
    run_speed_test()

    # Run the speed test when the button is clicked
    if st.button("Run Speed Test"):
        run_speed_test()

# Run the app
if __name__ == "__main__":
    main()

    # Schedule the speed test to run every 1 minute
    schedule.every(1).minutes.do(run_speed_test)

    # Main loop to run the scheduled speed test
    while True:
        schedule.run_pending()
        time.sleep(1)
