import bcrypt

def generate_bcrypt_hash(password: str, cost: int = 12) -> str:
    """
    Generate a bcrypt hash for a given password.

    Args:
        password (str): The password to hash.
        cost (int): The bcrypt cost factor (default is 12).

    Returns:
        str: The generated bcrypt hash.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate the salt with the specified cost factor
    salt = bcrypt.gensalt(cost)
    
    # Generate the bcrypt hash
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return the hash as a string
    return hashed.decode('utf-8')

if __name__ == "__main__":
    # Prompt the user to enter a password
    user_password = input("Enter the password to hash: ")
    
    # Generate the bcrypt hash
    bcrypt_hash = generate_bcrypt_hash(user_password)
    
    # Output the resulting hash
    print(f"The bcrypt hash is: {bcrypt_hash}")
