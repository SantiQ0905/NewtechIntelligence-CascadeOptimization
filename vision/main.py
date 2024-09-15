import cv2
import time
import datetime
import csv
from yolo_openVINO import YOLOv8_openVINO


def video_data():
    # Initialize the YOLOv8_openVINO model with the CPU device and video source (camera)
    model = YOLOv8_openVINO(device="CPU")

    cap = cv2.VideoCapture(0)

    # Create and open the CSV file for writing
    with open('detection_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["initial datetime", "final datetime", "time_worked(hr)"])

        last_print_time = time.time()
        start_time = datetime.datetime.now()
        interval_start_time = start_time
        detection_count = 0
        frame_count = 0

        if not cap.isOpened():
            print("Error: Could not open video stream.")
            exit()

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture image.")
                break

            # Perform inference
            frame, status = model.inference(frame)

            frame_count += 1
            if status:
                detection_count += 1

            # Check if two seconds have passed since the last print
            current_time = time.time()
            if current_time - last_print_time >= 10:
                interval_end_time = datetime.datetime.now()
                interval_duration = (interval_end_time - interval_start_time).total_seconds()
                detection_ratio = detection_count / frame_count  # ratio of detections to frames

                # Write the data to the CSV file
                writer.writerow([
                    interval_start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    interval_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    detection_ratio
                ])

                # Reset the interval start time, detection count, and frame count
                interval_start_time = interval_end_time
                detection_count = 0
                frame_count = 0
                last_print_time = current_time

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Check if 360 seconds have passed since the start time
            if (datetime.datetime.now() - start_time).seconds >= 31:
                break

    cap.release()
    cv2.destroyAllWindows()

    # Specify the file path
    file_path = 'detection_data.csv'

    # Read the CSV file and convert to string
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        csv_data = ""

        # Convert each row of CSV into a string format
        for row in csv_reader:
            csv_data += ";".join(row) + "\n"

    # Print or use the csv_data string
    return csv_data


import requests

if __name__ == '__main__':
    URL = "http://127.0.0.1:8000/tasks/consume/"
    requests.post(URL, data={"csv" : video_data(), "pk" : 2})