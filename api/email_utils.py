import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from fastapi import HTTPException

def send_email(to_email: str, subject: str, body: str):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "emailMulheresConectadas@gmail.com"
        from_password = "senha"

        msg = MIMEMultipart()
        msg["From"] = formataddr(("Equipe Mulheres Conectadas", from_email))
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {e}")
