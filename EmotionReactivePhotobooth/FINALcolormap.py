import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import socket

HOST = ''  # Listen on all available interfaces
PORT = 12345  # Use a non-reserved port number

# Load FER model
model = load_model('fer2013_mini_XCEPTION.102-0.66.hdf5', compile=False)

# Define emotion labels
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Define a dictionary to map emotions to colors
colors = {
    'Angry': 'red',     # red (255, 0, 0)
    'Disgust': 'yellow',   # yellow (255, 255, 0) 
    'Fear': 'magenta',      # magenta (255, 0, 255)
    'Happy': 'green',      # green (0, 255, 0)
    'Sad': 'blue',         # blue (0, 0, 255)
    'Surprise': 'orange',  # orange (255,127,80)
    'Neutral': 'white'     # white (255, 255, 255) 
}

# Initialize webcam capture
cap = cv2.VideoCapture(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Listening on {HOST}:{PORT}')
    conn, addr = s.accept()
    print(f'Connected by {addr}')

    while True:
        # Capture frame-by-frame
        ret, img = cap.read()

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop through each detected face
        for (x,y,w,h) in faces:
            # Extract the face ROI
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (64, 64), interpolation = cv2.INTER_AREA)

            # Preprocess the image for the FER model
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            img_pixels /= 255

            # Use the FER model to predict emotions
            # This returns a list of probabilities for each emotion.
            # Each probability represents the likelihood of the input image belonging to that emotion.
            predictions = model.predict(img_pixels)

            # Find the dominant emotion
            max_index = np.argmax(predictions[0])
            emotion1 = emotions[max_index]
            print(emotion1)

            # Get the indices of the three most probable emotions
            indices = np.argpartition(-predictions[0], 3)[:3]

            emotion1 = emotions[indices[0]]
            #emotion2 = emotions[indices[1]]
            #emotion3 = emotions[indices[2]]

            # Get the color associated with the dominant emotion
            color1 = colors[emotion1]
            #color2 = colors[emotion2]
            #color3 = colors[emotion3]
            

            # Send the color to Processing
            # message = str(color1) + "\n" + str(color2) + "\n" + str(color3)
            message = str(color1)
            conn.sendall(message.encode())

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()



