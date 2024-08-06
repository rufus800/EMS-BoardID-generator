import uuid
import hashlib
import logging

class IDGenerator:
    def __init__(self, database):
        self.database = database
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_unique_id(self, board_info):
        attempt = 0
        max_attempts = 10
        while attempt < max_attempts:
            # Use SHA-256 instead of MD5 for better security
            base_id = hashlib.sha256(str(board_info).encode()).hexdigest()[:12]
            unique_id = f"EMS-{base_id}-{str(uuid.uuid4())[:8]}"
            
            if not self.database.id_exists(unique_id):
                self.logger.info(f"Generated unique ID: {unique_id}")
                return unique_id
            
            attempt += 1
            self.logger.warning(f"ID collision occurred. Attempt {attempt} of {max_attempts}")

        self.logger.error("Failed to generate a unique ID after maximum attempts")
        raise Exception("Failed to generate a unique ID after maximum attempts")

    def validate_id(self, id_string):
        # Check if the ID matches the expected format
        if not id_string.startswith("EMS-") or len(id_string) != 29:
            return False
        
        # Check if the middle part is a valid hexadecimal string
        try:
            int(id_string[4:16], 16)
        except ValueError:
            return False
        
        # Check if the last part is a valid UUID4 fragment
        try:
            uuid.UUID(id_string[-8:], version=4)
        except ValueError:
            return False
        
        return True