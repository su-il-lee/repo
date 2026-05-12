import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import GMAIL_USER, GMAIL_APP_PW, RECIPIENTS
from datetime import datetime
import os

def send_mail(ppt_path):
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_USER
    msg["To"]      = ", ".join(RECIPIENTS)
    msg["Subject"] = f"[AI 뉴스 클리핑] {datetime.now().strftime('%Y년 %m월 %d일')} 주간"

    body = f"""안녕하세요,

이번 주 AI 뉴스 클리핑을 첨부해드립니다.
주요 섹션: AI 모델 동향 / 패션 AI / K-뷰티 AI / 규제·정책

확인 후 피드백 주시면 감사하겠습니다.
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # PPT 첨부
    with open(ppt_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)

    from email.utils import encode_rfc2231
    filename = os.path.basename(ppt_path)
    part.add_header("Content-Disposition", "attachment",
                filename=("utf-8", "", filename))
    msg.attach(part)
    # 교체 (587 포트)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PW)
        server.sendmail(GMAIL_USER, RECIPIENTS, msg.as_string())
    print("메일 발송 완료!")