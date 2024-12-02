import imaplib
import email
import os
from email import message_from_bytes
from email.header import decode_header

from datetime import datetime
import re

class EmailProcessor:
    def __init__(self, email_addr, password, imap_server, md_file):
        """Initialize the email processor"""
        self.email_addr = email_addr
        self.password = password
        self.imap_server = imap_server
        self.md_file = md_file
        
        # 创建与 md 文件同目录的 assets 文件夹
        md_dir = os.path.dirname(self.md_file)
        md_name = os.path.splitext(os.path.basename(self.md_file))[0]
        self.img_folder = os.path.join(md_dir, f"{md_name}.assets")
        
        # 创建图片目录
        if not os.path.exists(self.img_folder):
            os.makedirs(self.img_folder)

    def connect(self):
        """Connect to the email server"""
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_addr, self.password)
        _, _ = self.mail.select('INBOX')  # Correct ignored return value

    def get_emails(self):
        """Fetch email IDs"""
        _, messages = self.mail.search(None, 'ALL')
        return messages[0].split()

    def decode_str(self, s):
        """Decode email subject"""
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def process_email(self, email_id):
        """Process a single email"""
        _, msg_data = self.mail.fetch(email_id, '(RFC822)')
        email_body = msg_data[0][1]
        message = email.message_from_bytes(email_body)
        
        # Get email subject
        subject = self.decode_str(message['subject'])
        
        # Handle email content and attachments
        content = []
        attachments = []
        
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            fileName = part.get_filename()
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset()
                try:
                    payload = payload.decode(charset)
                except:
                    payload = payload.decode('utf-8')
                content.append(payload)
            elif fileName:
                attachments.append(part)
                
        return subject, '\n'.join(content), attachments

    def save_attachment(self, attachment):
        """Save image attachment"""
        filename = self.decode_str(attachment.get_filename())
        if filename:
            filepath = os.path.join(self.img_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(attachment.get_payload(decode=True))
            return filepath
        return None

    def delete_email(self, email_id):
        """Delete an email after processing"""
        self.mail.store(email_id, '+FLAGS', '\\Deleted')
        self.mail.expunge()

    def append_to_markdown(self, subject, content, image_paths):
        """Append content to Markdown file with timestamp"""
        sanitized_subject = re.sub(r'[^\w\-_\s.]','', subject).lower().replace(' ', '-')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        with open(self.md_file, 'a', encoding='utf-8') as f:
            f.write(f'\n## {subject} ({current_time})\n\n')  # 添加时间戳
            f.write(f'{content}\n\n')
            for img_path in image_paths:
                if img_path:
                    relative_path = os.path.relpath(img_path, os.path.dirname(self.md_file))
                    f.write(f'![{sanitized_subject}-{os.path.splitext(os.path.basename(img_path))[0]}]({relative_path})\n\n')

    def process_all_emails(self):
        """Process all emails and delete them after processing"""
        self.connect()
        for email_id in self.get_emails():
            try:
                subject, content, attachments = self.process_email(email_id)
                image_paths = [self.save_attachment(att) for att in attachments]
                self.append_to_markdown(subject, content, image_paths)
                self.delete_email(email_id)  # 处理完后删除邮件
            except Exception as e:
                print(f"Error processing email {email_id}: {str(e)}")
                continue
        self.mail.close()
        self.mail.logout()

# Example usage
if __name__ == "__main__":
    EMAIL = "shihuaidexianyu@yeah.net"
    PASSWORD = "EPRk4j4StzAmFExj"
    IMAP_SERVER = "imap.yeah.net"
    MD_FILE = os.path.join("docs", "想法", "output.md")  # Ensure correct path separation

    processor = EmailProcessor(EMAIL, PASSWORD, IMAP_SERVER, MD_FILE)
    processor.process_all_emails()
