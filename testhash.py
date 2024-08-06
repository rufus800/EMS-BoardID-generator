import bcrypt

# The password to check
password = b"adminpass"

# The provided hash
hashed = b"$2b$12$ek5SvNY9YNTWykQfiqlwY.627mTOGtC1hB4oRjwJTB8LXfHmvwL1m"

# Check if the provided hash matches the password
if bcrypt.checkpw(password, hashed):
    print("The password matches the hash.")
else:
    print("The password does not match the hash.")
