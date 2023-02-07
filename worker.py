import pika, os, time, sys
from dotenv import load_dotenv

load_dotenv()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    try:
        for t in range(int(body.decode())):
            sys.stdout.write(f"\r Processing... ({str(t + 1)})")
            sys.stdout.flush()
            time.sleep(1)
        print("\n Done Computing")
    except ValueError:
        pass
    print("=============================================================")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # mempertahankan pesan di rabbitMQ walaupun receiver meninggoy


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

print("Masukkan nama queue channel untuk menerima pesan melalui RMQ.")
queue_name = input(">> channel: ")
channel.queue_declare(
    queue=queue_name,  # nama queue
    durable=True  # untuk mempertahankan queue meskipun server rabbitMQ berhenti
)

# consume pesan (menerima)
channel.basic_qos(prefetch_count=1)  # hanya akan memberikan satu tugas dulu sampe selesai
channel.basic_consume(
    queue=queue_name,  # nama queue
    on_message_callback=callback  # memanggil fungsi callback
)

print('Menunggu pesan masuk... (CTRL+C to close)')
channel.start_consuming()  # bersifat standby
