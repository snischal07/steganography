import cv2
import os
import hashlib

# Function to encrypt the secret message
def encrypt_message(secret_message, password):
    key = hashlib.sha256(password.encode()).digest()
    encrypted_message = []
    for i in range(len(secret_message)):
        encrypted_char = chr(ord(secret_message[i]) ^ key[i % len(key)])
        encrypted_message.append(encrypted_char)
    return ''.join(encrypted_message)

# Function to decrypt the secret message
def decrypt_message(encrypted_message, password):
    return encrypt_message(encrypted_message, password)

# Hide an encrypted message in an image
def hide_message_in_image(image_path, encrypted_message):
    img = cv2.imread(image_path)
    n, m, z = 0, 0, 0

    for i in range(len(encrypted_message)):
        img[n, m, z] = ord(encrypted_message[i])
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    image_dir, image_filename = os.path.split(image_path)
    encrypted_image_path = os.path.join(image_dir, "encrypted_" + image_filename)
    cv2.imwrite(encrypted_image_path, img)
    return encrypted_image_path

# Main function to handle user input and interaction
def main():
    image_path = input("Enter the path of the image: ")
    password = input("Enter the password: ")
    secret_message = input("Enter the secret message: ")

    encrypted_message = encrypt_message(secret_message, password)
    encrypted_image_path = hide_message_in_image(image_path, encrypted_message)

    print("Message encrypted and hidden in the image.")
    print("Encrypted image saved as:", encrypted_image_path)

    passcode = input("Enter the passcode for decryption: ")
    
    if hashlib.sha256(passcode.encode()).digest() == hashlib.sha256(password.encode()).digest():
        img = cv2.imread(encrypted_image_path)
        decrypted_message = decrypt_message(encrypted_message, passcode)
        print("Decrypted message:", decrypted_message)
    else:
        print("Invalid passcode.")

if __name__ == "__main__":
    main()
