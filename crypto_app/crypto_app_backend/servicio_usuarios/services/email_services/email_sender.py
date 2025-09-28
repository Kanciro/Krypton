

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os

# Configuración del servidor de correo
# Es VITAL que uses variables de entorno para las credenciales
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "tu_correo@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "tu_contraseña_de_app")
SMTP_SERVER = "smtp.gmail.com"  # Ejemplo para Gmail
SMTP_PORT = 587

def send_verification_email(receiver_email: str, code: str):
    """
    Envía un correo electrónico con un código de verificación.
    """
    # El asunto debe ser un objeto Header para manejar la codificación correctamente
    subject = Header("Código de verificación para tu cuenta Krypton", 'utf-8')
    body = f"""
    Hola,

    Has solicitado cambiar el correo electrónico de tu cuenta.
    Usa el siguiente código para verificar tu identidad:

    {code}

    Si no has solicitado este cambio, por favor ignora este correo.

    Saludos,
    El equipo de Krypton
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email
    msg['Subject'] = str(subject)
    msg.attach(MIMEText(body, 'plain', _charset="utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Habilita la seguridad TLS
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Correo de verificación enviado a {receiver_email}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
    


# servicio_usuarios/services/email_service/email_sender.py

# ... tus imports existentes

# servicio_usuarios/services/email_service/email_sender.py

# ... tus imports existentes
# ... tus funciones

def send_registration_email_with_code(receiver_email: str, code: str):
    """
    Envía un correo electrónico de bienvenida con un código de verificación.
    """
    subject = Header("¡Bienvenido a Krypton! Tu código de verificación", 'utf-8')
    body = f"""
    Hola,

    Gracias por registrarte en Krypton. Para activar tu cuenta, por favor ingresa el siguiente código en la aplicación:

    {code}

    Si no has solicitado este registro, por favor ignora este correo.

    Saludos,
    El equipo de Krypton
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email
    msg['Subject'] = str(subject)
    msg.attach(MIMEText(body, 'plain', _charset="utf-8"))

    print(f"Código de verificación generado (SOLO PARA PRUEBAS): {code}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Correo de registro enviado a {receiver_email}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo de registro: {e}")
        return False

# Mantén tus otras funciones de envío de correo si las necesitas.
# Elimina `send_registration_email` si solo usarás el código.