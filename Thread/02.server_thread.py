# import socket, sys, traceback dan threading
import socket
import sys
import traceback
import threading

# jalankan server
def main():
    start_server()

# fungsi saat server dijalankan
def start_server():
    # tentukan IP server
    ip = 'localhost'
    
    # tentukan port server
    port = 8080

    # buat socket bertipe TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # option socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket dibuat")

    # lakukan bind
    try:
        s.bind((ip,port))
    except:
        # exit pada saat error
        print("Bind gagal. Error : " + str(sys.exc_info()))
        sys.exit()

    # listen hingga 5 antrian
    s.listen(5)
    print("Socket mendengarkan")

    # infinite loop, jangan reset setiap ada request
    while True:
        # terima koneksi
        c, addr = s.accept()
        
        # dapatkan IP dan port
        client_ip = str(addr[0])
        client_port = str(addr[1])
        print(client_ip+', '+client_port+' connected')

        # jalankan thread untuk setiap koneksi yang terhubung
        try:
            t = threading.Thread(name='client_thread', target=client_thread, args=(c, client_ip, client_port))
            t.start()
        except:
            # print kesalahan jika thread tidak berhasil dijalankan
            print("Thread tidak berjalan.")
            traceback.print_exc()

    # tutup socket
    s.close() 


def client_thread(connection, ip, port, max_buffer_size = 4096):
    # flag koneksi
    is_active = connection

    # selama koneksi aktif
    while is_active:

        # terima pesan dari client
        data = connection.recv(max_buffer_size)

        # dapatkan ukuran pesan
        client_input_size = len(data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        
        # print jika pesan terlalu besar
        if client_input_size > max_buffer_size:
            print("The input size is greater than expected {}")

        # dapatkan pesan setelah didecode
        client_input = data.decode()
        
        # jika "quit" maka flag koneksi = false, matikan koneksi
        if "quit" in client_input:
            # ubah flag
            is_active = False
            print("Client meminta keluar")
            
            # matikan koneksi
            connection.close()
            print("Connection " + ip + ":" + port + " ditutup")
            
        else:
            # tampilkan pesan dari client
            print(ip+', '+port+' : '+client_input)
            
# panggil fungsi utama
if __name__ == "__main__":
    main()