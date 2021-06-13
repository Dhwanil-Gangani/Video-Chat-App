#Client 2
import socket, cv2, numpy , threading

#Send
def send():
        server_socket = socket.socket()
        #To Reuse The Port Again
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        serverip = "192.168.0.103"
        serverport = 1465
        #Connect with Client A 
        server_socket.connect((serverip,serverport))
        #Capture Video and Store Data in video var
        video = cv2.VideoCapture(0)
        while True:
            #Read the Data
            ret, frame = video.read()
            #Reshape It
            frame = frame.reshape((480, 640,3))
            #Resize other Window
            cv2.namedWindow('Video2', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Video2', 180,180)
            cv2.imshow('Video2' , frame)
            #Convert Data to Bytes 
            data = frame.tostring()
            if cv2.waitKey(110) == 13:
                video.release()
                server_socket.close()
                break
            #Send Data to Client A
            server_socket.sendto(data,(serverip,serverport))
        cv2.destroyAllWindows()
        
#Recive
def reciver():
    client_socket = socket.socket()
    #To Reuse The Port Again
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    port = 1412
    ip = ""
    client_socket.bind((ip,port))
    client_socket.listen()
    session , address = client_socket.accept()
    while True:
        data = session.recv(921600)
        #Convert Bytes data in Numpy Array
        frame = numpy.fromstring(data , numpy.uint8)
        #Reshape 1D array to 2D array
        array_2d = numpy.reshape(frame, (-1, 2))
        #Reshape to 3D Array
        array_3d = array_2d.reshape((480, 640,3))
        #Image Recived From Server
        cv2.imshow('Video1' , array_3d)
        #Terminate Image
        if cv2.waitKey(110) == 13:
            print("Connection Closed!")
            break
        else:
            pass
    cv2.destroyAllWindows()
    

threading.Thread(target=send).start()
threading.Thread(target=reciver).start()