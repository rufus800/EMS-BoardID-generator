import serial
import json
import logging

class BoardManager:
    def __init__(self, database, port='/dev/ttyUSB0', baudrate=9600):
        self.database = database
        self.port = port
        self.baudrate = baudrate
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def read_board_info(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=5) as ser:
                ser.write(b'GET_INFO\n')
                response = ser.readline().decode('utf-8').strip()
                if not response:
                    raise ValueError("No response received from the board")
                board_info = json.loads(response)
                return board_info
        except serial.SerialException as e:
            self.logger.error(f"Serial communication error: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding board information: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error reading board info: {e}")
            raise

    def store_board_info(self, board_info):
        try:
            result = self.database.insert_board(board_info)
            if result:
                self.logger.info(f"Board information stored successfully: {board_info['id']}")
            else:
                self.logger.warning(f"Failed to store board information: {board_info['id']}")
            return result
        except Exception as e:
            self.logger.error(f"Error storing board information: {e}")
            raise

    def get_all_boards(self):
        try:
            boards = self.database.get_all_boards()
            self.logger.info(f"Retrieved {len(boards)} boards from the database")
            return boards
        except Exception as e:
            self.logger.error(f"Error retrieving boards: {e}")
            raise

    def update_board_info(self, board_id, updated_info):
        try:
            result = self.database.update_board(board_id, updated_info)
            if result:
                self.logger.info(f"Board information updated successfully: {board_id}")
            else:
                self.logger.warning(f"Failed to update board information: {board_id}")
            return result
        except Exception as e:
            self.logger.error(f"Error updating board information: {e}")
            raise

    def delete_board(self, board_id):
        try:
            result = self.database.delete_board(board_id)
            if result:
                self.logger.info(f"Board deleted successfully: {board_id}")
            else:
                self.logger.warning(f"Failed to delete board: {board_id}")
            return result
        except Exception as e:
            self.logger.error(f"Error deleting board: {e}")
            raise