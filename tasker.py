import pika
import os
from dotenv import load_dotenv

load_dotenv()

input("Tekan [enter] untuk inisialisasi RMQ parameters.")
credential = pika.PlainCredentials(os.getenv("user"), os.getenv("pass"))
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv("host"),
    port=int(os.getenv("port")),
    virtual_host=os.getenv("vhost"),
    credentials=credential
))
print(">> Inisialisasi RMQ parameters berhasil!!")
print("=============================================================")

input("Tekan [enter] untuk membuka koneksi ke RMQ.")
channel = connection.channel()
print(">> Koneksi ke RMQ berhasil dibuka!!")
print("=============================================================")

print("Masukkan nama queue channel untuk mengirim pesan melalui RMQ.")
queue_name = input(">> channel: ")
channel.queue_declare(
    queue=queue_name,  # menentukan nama queue
    durable=True  # param untuk mempertahankan queue meskipun server rabbitMQ berhenti
)

# publish pesan (mengirim)
print("Masukkan tujuan dan pesan yang akan dikirim atau ketik 'exit' to close.")
while True:
    tujuan = input(f">> tujuan: ")
    if tujuan == 'exit':
        break
    message = input(">> pesan: ")
    if message == 'exit':
        break

    channel.basic_publish(
        exchange='',
        routing_key=tujuan,  # nama queue
        body=message,  # isi pesan dari queue yang dikirim
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)  # pesan disimpan di cache
    )
    print(f" [x] Sent to {tujuan}")
connection.close()  # menutup koneksi setelah mengirim pesan
