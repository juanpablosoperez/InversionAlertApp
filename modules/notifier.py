import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar el correo (puedes usar variables de entorno para mayor seguridad)
EMAIL_SENDER = "soperezjuanpablo1@gmail.com"
EMAIL_PASSWORD = "h v r o v l e b p h s h j b r q"
EMAIL_RECIPIENT = "juanpsoperez@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Puerto para TLS

def enviar_notificacion(ticker, precio_actual, precio_objetivo):
    """Envía una notificación por email cuando el precio actual alcanza el objetivo."""
    try:
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECIPIENT
        msg["Subject"] = f"📈 Alerta: {ticker} alcanzó el precio objetivo"

        body = f"""
        🔔 Notificación de Inversión 🔔
        
        ✅ Ticker: {ticker}
        💰 Precio Actual: {precio_actual}
        🎯 Precio Objetivo: {precio_objetivo}
        
        ¡Revisa tu portafolio!
        """
        msg.attach(MIMEText(body, "plain"))

        # Conectar con el servidor SMTP y enviar email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        server.quit()

        print(f"✅ Notificación enviada para {ticker}")

    except Exception as e:
        print(f"❌ Error al enviar notificación: {e}")
