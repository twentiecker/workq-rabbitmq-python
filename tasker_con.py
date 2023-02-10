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

# publish pesan (mengirim)
print("Masukkan tujuan dan pesan yang akan dikirim atau ketik 'exit' to close.")
while True:
    tujuan = input(f">> tujuan: ")
    if tujuan == 'exit':
        break
    message = input(">> pesan (angka): ")
    if message == 'exit':
        break

    channel.queue_declare(
        queue=tujuan,  # menentukan nama queue
        durable=True  # param untuk mempertahankan queue meskipun server rabbitMQ berhenti
    )

    channel.basic_publish(
        exchange='',
        routing_key=tujuan,  # nama queue
        body=message,  # isi pesan dari queue yang dikirim
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)  # pesan disimpan di cache
    )
    print(f" [x] Sent to {tujuan}")
connection.close()  # menutup koneksi setelah mengirim pesan
