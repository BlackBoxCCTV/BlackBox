# client_secure.py
import socket, ssl, cv2, pickle, struct
from cryptography.fernet import Fernet

# AES key (shared securely in advance)
key = b'KEYTEST'  # use above method to get it
fernet = Fernet(key)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # For dev; use proper certs in production

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock)
secure_sock.connect(('server_ip', 9999))  # replace with real IP

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Serialize + encrypt
    data = pickle.dumps(frame)
    encrypted = fernet.encrypt(data)
    message = struct.pack("Q", len(encrypted)) + encrypted
    secure_sock.sendall(message)

    cv2.imshow("Client Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
secure_sock.close()
cv2.destroyAllWindows()