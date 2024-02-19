# Text Recognition and Database Storage

This application allows users to upload images containing text, performs text recognition using Tesseract OCR, and provides options to manipulate and store the extracted text and associated images.

![Project Screenshots](https://github.com/mannan-python-developer/Text-Recognition-using-OpenCV-and-Tesseract-OCR-/blob/main/Text%20Recognition.png)

## Features:

- **Image Upload**: Users can upload images in common formats like PNG, JPG, and BMP.

- **Text Recognition**: The uploaded image is processed to extract text using the Tesseract OCR engine.

- **Text and Image Display**: The extracted text is displayed to the user alongside the uploaded image for verification and manipulation.

- **Database Storage**: Text data along with the associated images can be stored in a MySQL database for future reference.

- **Error Handling**: The application incorporates error handling for various scenarios, such as database connection issues or empty text fields.

## Technologies Used:

- **Python**: The application is primarily developed in Python, leveraging libraries such as OpenCV, PyQt5, and PyTesseract.

- **OpenCV**: Utilized for image processing tasks, including converting images to grayscale.

- **PyTesseract**: Used for optical character recognition (OCR) to extract text from images.

- **PyQt5**: Employed for creating the graphical user interface (GUI) and handling user interactions.

- **MySQL Connector**: Facilitates communication with the MySQL database for data storage.

## Usage:

1. **Installation**: Ensure Python and the required libraries are installed. Install Tesseract OCR and MySQL Server if not already installed.

2. **Database Setup**: Import the provided database file into MySQL Workbench and configure the database connection settings in the code.

3. **Execution**: Run the Python script. Upon execution, the GUI will be displayed, allowing users to upload images and interact with the application.

4. **Image Upload and Text Extraction**: Choose an image file containing text. The application will extract text using OCR and display it alongside the image.

5. **Database Storage**: Optionally, users can save the extracted text and associated images into the configured MySQL database for archival purposes.

6. **Error Handling**: The application handles various errors gracefully and provides informative messages to the user in case of any issues encountered during execution.


## License:

This project is licensed under the [MIT License](LICENSE).
