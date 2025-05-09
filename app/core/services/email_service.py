import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings
from app.core.utils.templates import render_template

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails."""

    @staticmethod
    async def send_email(to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send an email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            is_html: Whether body contains HTML

        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.EMAIL_FROM
            msg["To"] = to_email
            msg["Subject"] = subject

            content_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, content_type))

            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=settings.EMAIL_TIMEOUT) as server:
                server.ehlo()
                server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.exception("Error sending email: %s", e)
            return False

    @staticmethod
    async def send_verification_email(to_email: str, otp: str) -> bool:
        """Send email verification OTP.

        Args:
            to_email: Recipient email address
            otp: One-time password for verification

        Returns:
            True if email was sent successfully, False otherwise
        """
        subject = "MeetingApp - Подтверждение электронной почты"

        html_body = render_template(
            "email/verification.html",
            {"otp": otp},
        )

        return await EmailService.send_email(to_email, subject, html_body, is_html=True)
