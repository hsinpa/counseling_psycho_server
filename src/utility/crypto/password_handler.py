from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os

SERVER_HASH_KEY = os.environ.get('ACCOUNT_HASH_KEY').encode('utf-8')

# Configure Argon2id hasher with lower memory requirements
# These parameters are adjusted for servers with limited resources
ph = PasswordHasher(
    time_cost=6,          # Increased iterations to compensate for lower memory
    memory_cost=4096,     # Memory usage in KiB (8 MB instead of 64 MB)
    parallelism=2,
)

def encode_password(password: str) -> str:
    """
    Encode a password using Argon2id with a random salt

    Args:
        password (str): The password to encode

    Returns:
        Full Argon2id hash (includes algorithm, parameters, salt, and hash),
    """
    # Ensure password is a string
    if not isinstance(password, str):
        password = str(password)

    # Combine the password with the server hash key for extra security
    # Convert server key to hex string to safely combine with password
    server_key_hex = SERVER_HASH_KEY.hex()
    enhanced_password = f"{password}${server_key_hex}"

    # Hash the enhanced password using Argon2id
    # The salt is automatically generated and included in the hash string
    argon2_hash = ph.hash(enhanced_password)

    # Return the complete hash (contains algorithm, parameters, salt, and hash)
    return argon2_hash


def verify_password(password: str, stored_hash: str):
    """
    Verify a password against a stored Argon2id hash

    Args:
        password (str): The password to verify
        stored_hash (str): The complete Argon2id hash string

    Returns:
        bool: True if password matches, False otherwise
    """
    # Ensure password is a string
    if not isinstance(password, str):
        password = str(password)

    # Combine with server key (same as during encoding)
    server_key_hex = SERVER_HASH_KEY.hex()
    enhanced_password = f"{password}${server_key_hex}"

    try:
        # Verify the password - this uses constant-time comparison internally
        ph.verify(stored_hash, enhanced_password)
        return True
    except VerifyMismatchError:
        # Password doesn't match
        return False
    except Exception as e:
        # Handle any other exceptions (corrupted hash, etc.)
        print(f"Error verifying password: {e}")
        return False