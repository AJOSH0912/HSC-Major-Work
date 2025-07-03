import pandas as pd
from cryptography.fernet import Fernet
import os

#Generate a key for encryption/decryption.
def generate_key():
    key = Fernet.generate_key()
    return key

#Saves the encryption key to a file.
def save_key(key, key_file_path):

    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Key saved to: {key_file_path}")

#Loads the encryption key from a file.
def load_key(key_file_path):

    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"Key file not found: {key_file_path}")
    
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
    return key

# Encrypts a file using the provided key or key file path. This function is called from encrypt_csv_file.

def encrypt_file(file_path, key_file_path=None, key=None):

    # Get encryption key
    if key is None:
        if key_file_path is None:
            raise ValueError("Either key or key_file_path must be provided")
        key = load_key(key_file_path)
    
    # Create Fernet object
    fernet = Fernet(key)
    
    # Read the file to encrypt
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Encrypt the data
    encrypted_data = fernet.encrypt(file_data)
    
    # Save encrypted file
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    print(f"File encrypted: {file_path} -> {encrypted_file_path}")
    os.remove(file_path)  # Optionally remove the original file after encryption
    return encrypted_file_path

# Decrypts a file using the provided key or key file path. This function is called from decrypt_csv_file.
def decrypt_file(encrypted_file_path, key_file_path=None, key=None, output_path=None):

    # Get decryption key
    if key is None:
        if key_file_path is None:
            raise ValueError("Either key or key_file_path must be provided")
        key = load_key(key_file_path)
    
    # Create Fernet object
    fernet = Fernet(key)
    
    # Read the encrypted file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    try:
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Determine output path
        if output_path is None:
            output_path = encrypted_file_path.replace('.encrypted', '_decrypted')
            if encrypted_file_path.endswith('.encrypted'):
                output_path = encrypted_file_path[:-10]  # Remove .encrypted extension
        
        # Save decrypted file
        with open(output_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        print(f"File decrypted: {encrypted_file_path} -> {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

# Specifically encrypt CSV files and return the path to the encrypted file.
def encrypt_csv_file(csv_file_path, key_file_path=None, key=None):

    if not csv_file_path.endswith('.csv'):
        raise ValueError("File must be a CSV file")
    
    return encrypt_file(csv_file_path, key_file_path, key)

# Specifically decrypt CSV files and return the path to the decrypted file. 
# Once file is decrypted load data to dataframe and then remove the decrypted file.
def decrypt_csv_file(encrypted_csv_path, key_file_path=None, key=None):

    decrypted_path = decrypt_file(encrypted_csv_path, key_file_path, key)
    print(f"Decrypted file path: {decrypted_path}")
    if decrypted_path:
        df = pd.read_csv(decrypted_path)
        # Optionally remove decrypted file for security
        os.remove(decrypted_path)
        print(f"CSV loaded and temporary file removed: {decrypted_path}")
        return df
    else:
        return None

