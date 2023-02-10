import tkinter as tk
import pika
import os
from dotenv import load_dotenv


# membuat fungsi connect
def connect():
    credential = pika.PlainCredentials(os.getenv("user"), os.getenv("pass"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("host"),
        port=int(os.getenv("port")),
        virtual_host=os.getenv("vhost"),
        credentials=credential
    ))
    btn_connect.config(state="disabled")
    # mengaktifkan label, button, text
    lbl_status.config(text="Connected!", state="active")
    btn_kirim.config(state="active")
    lbl_pesan.config(state="active")
    txt_pesan.config(state="normal")
    lbl_tujuan.config(state="active")
    txt_tujuan.config(state="normal")
    btn_disconnect.config(state="active")
    return connection


# membuat fungsi kirim data
def kirim():
    channel = connect().channel()
    channel.queue_declare(
        queue=txt_tujuan.get(),  # menentukan nama queue
        durable=True  # param untuk mempertahankan queue meskipun server rabbitMQ berhenti
    )
    channel.basic_publish(
        exchange='',
        routing_key=txt_tujuan.get(),  # nama queue
        body=txt_pesan.get(),  # isi pesan dari queue yang dikirim
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)  # pesan disimpan di cache
    )


# membuat fungsi disconnect
def disconnect():
    connect().close()  # menutup koneksi setelah mengirim pesan
    # menghapus isian text
    txt_pesan.delete(0, tk.END)
    txt_tujuan.delete(0, tk.END)
    btn_connect.config(state="active")
    # menonaktifkan label, button, text
    lbl_status.config(text="Disconnected!", state="disabled")
    btn_kirim.config(state="disabled")
    lbl_pesan.config(state="disabled")
    txt_pesan.config(state="disabled")
    txt_pesan.config(state="disabled")
    lbl_tujuan.config(state="disabled")
    txt_tujuan.config(state="disabled")
    btn_disconnect.config(state="disabled")


load_dotenv()

# membuat window
app = tk.Tk()
app.geometry("300x230")
app.title("Tasker")

# membuat garis
C = tk.Canvas(height=230, width=300)
line = C.create_line(10, 170, 290, 170, fill="#a2a39c", width=2)
C.pack()

# membuat label dan text tujuan
lbl_tujuan = tk.Label(text="Tujuan", state="disabled")
lbl_tujuan.place(x=10, y=60)
txt_tujuan = tk.Entry(state="disabled")
txt_tujuan.place(x=10, y=85)

# membuat label dan text pesan
lbl_pesan = tk.Label(text="Pesan (angka)", state="disabled")
lbl_pesan.place(x=150, y=60)
txt_pesan = tk.Entry(state="disabled")
txt_pesan.place(x=150, y=85)

# membuat status koneksi
lbl_status = tk.Label(text="Disconnected!", state="disabled")
lbl_status.place(x=70, y=20)

# membuat tombol connect
btn_connect = tk.Button(text="Connect", command=connect)
btn_connect.place(x=10, y=20)

# membuat tombol kirim data
btn_kirim = tk.Button(text="Kirim Data", command=kirim, state="disabled")
btn_kirim.place(x=10, y=125)

# membuat tombol disconnect
btn_disconnect = tk.Button(text="Disconnect", command=disconnect, state="disabled")
btn_disconnect.place(x=10, y=190)

# menjalankan window
app.mainloop()
