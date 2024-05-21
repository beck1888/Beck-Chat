ALPHANUMERIC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
ALPHA_LEN = len(ALPHANUMERIC)

def generate_numeric_key(key):
    return [ord(char) for char in key]

def encrypt(plain_text, key):
    numeric_key = generate_numeric_key(key)
    key_len = len(numeric_key)
    
    encrypted_text = []
    for i, char in enumerate(plain_text):
        if char in ALPHANUMERIC:
            shift = numeric_key[i % key_len]
            encrypted_char = ALPHANUMERIC[(ALPHANUMERIC.index(char) + shift) % ALPHA_LEN]
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def decrypt(encrypted_text, key):
    numeric_key = generate_numeric_key(key)
    key_len = len(numeric_key)
    
    decrypted_text = []
    for i, char in enumerate(encrypted_text):
        if char in ALPHANUMERIC:
            shift = numeric_key[i % key_len]
            decrypted_char = ALPHANUMERIC[(ALPHANUMERIC.index(char) - shift) % ALPHA_LEN]
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)
