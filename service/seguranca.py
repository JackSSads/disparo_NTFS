import base64

def encrypt_password(password: str) -> str:
    """Criptografa uma senha usando Base64."""
    # Converte a string para bytes
    password_bytes = password.encode('utf-8')
    # Criptografa usando Base64
    encrypted_bytes = base64.b64encode(password_bytes)
    # Converte de volta para string
    encrypted_password = encrypted_bytes.decode('utf-8')
    return encrypted_password

def decrypt_password(encrypted_password: str) -> str:
    """Descriptografa uma senha codificada em Base64."""
    # Converte a string para bytes
    encrypted_bytes = encrypted_password.encode('utf-8')
    # Descriptografa usando Base64
    decrypted_bytes = base64.b64decode(encrypted_bytes)
    # Converte de volta para string
    decrypted_password = decrypted_bytes.decode('utf-8')
    return decrypted_password
