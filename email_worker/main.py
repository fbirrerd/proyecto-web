import time
import psycopg2
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_email(to, subject, body):
    # Configuración del servidor SMTP
    smtp_server = "mailserver"
    smtp_port = 587
    from_email = "youremail@midominio.com"
    password = "yourpassword"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def process_pending_emails():
    # Conectar a Redis para obtener correos pendientes
    r = redis.StrictRedis(host='redis_db', port=6379, db=0)

    # Conectar a PostgreSQL para obtener los correos pendientes
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_EMAIL_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='postgres_email',
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = conn.cursor()

    while True:
        # Buscar 10 correos pendientes
        cursor.execute("SELECT * FROM emails WHERE status = 'pending' LIMIT 10")
        emails = cursor.fetchall()

        for email in emails:
            email_id, recipient, cc, bcc, subject, body, status, error, created_at, updated_at = email
            if send_email(recipient, subject, body):
                cursor.execute("""
                    UPDATE emails SET status = 'sent' WHERE id = %s
                """, (email_id,))
            else:
                cursor.execute("""
                    UPDATE emails SET status = 'error', error = %s WHERE id = %s
                """, ("Error al enviar correo", email_id))

        conn.commit()
        time.sleep(60)  # Esperar 1 minuto para procesar otros correos

if __name__ == "__main__":
    process_pending_emails()
