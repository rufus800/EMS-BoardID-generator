import bcrypt

# In a real-world application, you would store these securely, not in the code
USERS = {
    'admin': b'$2b$12$ek5SvNY9YNTWykQfiqlwY.627mTOGtC1hB4oRjwJTB8LXfHmvwL1m'  # password: adminpass
}

def verify_password(username, password):
    if username not in USERS:
        return False
    
    stored_hash = USERS[username]
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())