# EMS Board ID Generator

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Board Detection](#board-detection)
7. [Data Management](#data-management)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

The EMS Board ID Generator is a comprehensive software solution designed to manage and track electronic manufacturing services (EMS) boards. This application allows users to generate unique IDs for boards, store board information, and manage a database of board details. It features a graphical user interface for easy interaction and supports both manual data entry and automated board detection.

## Features

- Secure user authentication
- Automatic board detection via serial connection
- Generation of unique board IDs
- Manual data entry for board information
- Database storage and retrieval of board data
- Search functionality for stored board information
- Export and import capabilities using CSV format
- User-friendly graphical interface

## System Requirements

- Python 3.6 or higher
- PyQt5
- pyserial
- SQLite3
- Operating System: Windows, macOS, or Linux

## Installation

1. Clone the repository:
   ```
   git clone repo_url
   ```

2. Navigate to the project directory:
   ```
   cd ems-board-id-generator
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the application, run the following command in the project directory:

```
python main.py
```

This will launch the login window. After successful authentication, you'll be presented with the main application window.

To make into linux executable

```
rm -rf build dist && pyinstaller ems_board_id_generator.spec && cd dist/ems_board_id_generator && ./ems_board_id_generator
```

## Board Detection

The EMS Board ID Generator includes an automated board detection feature that works as follows:

1. **Serial Connection**: The application attempts to establish a serial connection with the board using the pyserial library. By default, it looks for a connection on `/dev/ttyUSB0` with a baud rate of 9600.

2. **Connection Check**: The `check_board_connection()` method in the `MainWindow` class periodically checks if a board is connected. If a connection is successful, the status is updated to "Connected" and displayed in green. If no connection is detected, the status shows "Not Connected" in red.

3. **Board Information Retrieval**: When a board is detected, the `read_board_info()` method in the `BoardManager` class is used to request information from the board. It sends a `GET_INFO` command to the board and expects a JSON response containing the board's details.

4. **Data Parsing**: The received JSON data is parsed and stored in the application's database using the `store_board_info()` method.

5. **Error Handling**: The system includes error handling for various scenarios such as connection failures, timeout issues, or invalid data received from the board.

To ensure proper board detection:
- Make sure the board is properly connected to the computer.
- Verify that the correct serial port is being used (you may need to adjust the port in the code if it's different from `/dev/ttyUSB0`).
- Ensure the board is programmed to respond to the `GET_INFO` command with the appropriate JSON-formatted data.

## Data Management

### Data Entry
- The "Data Entry" tab allows users to manually input board information.
- Fields include Board Name, Board Type, Manufacturer, Manufacture Date, and Notes.
- Clicking "Generate ID" creates a unique ID for the board and stores the information.

### Data View
- The "Data View" tab displays all stored board information in a table format.
- Users can search for specific boards using the search functionality.
- The table can be sorted by clicking on column headers.

### Import/Export
- The application supports importing and exporting data in CSV format.
- To export, click the "Export to CSV" button and choose a save location.
- To import, click the "Import from CSV" button and select a CSV file to import.

## Security

- User authentication is required to access the application.
- Passwords are securely hashed and verified using the `verify_password()` function in the `security.py` module.
- The SQLite database is used to store board information securely.

## Troubleshooting

- If board detection fails, check the physical connection and ensure the correct serial port is specified.
- For database issues, verify that the SQLite database file has the correct permissions.
- If the application crashes, check the console for error messages that may provide more information.

## Contributing

Contributions to the EMS Board ID Generator are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear, descriptive commit messages.
4. Push your branch and submit a pull request.


