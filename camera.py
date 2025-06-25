# client_secure.py
import socket, ssl, cv2, pickle, struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('127.0.0.1', 25565))  # replace with real IP

cap = cv2.VideoCapture(0)

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Serialize + encrypt
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        sock.sendall(message)

    cap.release()
    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()