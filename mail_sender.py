import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from file_manager import sanitize_filename

def read_contact_email(file_path):
    """
    Lit le fichier de configuration du contact et extrait l'adresse e-mail.
    :param file_path: Chemin du fichier de configuration du contact.
    :return: L'adresse e-mail ou None si elle n'est pas définie.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("mail="):
                    email = line.strip().split("=")[1].replace('"', '').strip()
                    return email if email else None
    except FileNotFoundError:
        print(f"⚠ Fichier non trouvé : {file_path}")
    
    return None


def send_mail(to_email, subject, messages_list):
    """
    Envoie un e-mail avec les messages non lus sous forme de liste.
    :param to_email: Adresse e-mail du destinataire.
    :param subject: Sujet de l'e-mail.
    :param messages_list: Liste contenant les messages.
    """
    # ⚠ Modifier ces informations avec les vraies
    smtp_server = "ssl0.ovh.net"  # Ex: smtp.gmail.com
    smtp_port = 465 # SSL/TLS
    sender_email = "YOUR_LOGIN"  # Your login or mail adress
    sender_password = "YOUR_PASSWD"

    try:
        # Make the message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Make list of message
        message_body = "\n".join(messages_list)
        msg.attach(MIMEText(message_body, "plain"))

        # 🔹 Connect to server
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # To usse STARTTLS
        # server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        print(f"E-mail envoyé à {to_email}")

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")