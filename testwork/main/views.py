from django.shortcuts import render
from .models import Message
from django.http import HttpResponse

import imaplib
import email
from email.header import decode_header
from django.utils import timezone
from .models import Message, Attachment
import logging

logger = logging.getLogger(__name__)
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'main/message_list.html', {'messages': messages})


def fetch_emails(request):
    fetch_and_save_messages()

    return HttpResponse("Emails have been fetched and saved successfully.")


def fetch_and_save_messages():
    imap_server = ''
    email_user = ''
    email_pass = ''

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)

        mail.select('inbox')

        status, messages = mail.search(None, 'ALL')
        mail_ids = messages[0].split()

        logger.info(f"Found {len(mail_ids)} emails.")

        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            if status != 'OK':
                logger.error(f"Failed to fetch email id {mail_id}")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            date_sent = email.utils.parsedate_to_datetime(msg['Date'])
            date_received = timezone.now()

            message_instance = Message.objects.create(
                subject=subject,
                date_sent=date_sent,
                date_received=date_received,
                message_text=msg.get_payload(decode=True).decode() if not msg.is_multipart() else '',
                source='yandex'
            )

            logger.info(f"Saved message with subject: {subject}")  # Логирование

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    if filename:
                        attachment = Attachment(message=message_instance)
                        attachment.file.save(filename, part.get_payload(decode=True))
                        attachment.save()

                        logger.info(f"Saved attachment: {filename}")  # Логирование

        mail.logout()
    except imaplib.IMAP4.error as e:
        logger.error(f"IMAP4 error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
