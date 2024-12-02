import imaplib
import email
import os
from email import message_from_bytes
from email.header import decode_header

from datetime import datetime
import re
import subprocess
import time  # 用于添加延时

class EmailProcessor:
    def __init__(self, email_addr, password, imap_server, md_file):
        """初始化邮件处理器"""
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
        
        # 初始化日志文件路径
        self.log_file = os.path.join(md_dir, 'log.md')
        self.initialize_log()

    def initialize_log(self):
        """初始化日志文件，如果不存在则创建"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("# Email Processor Log\n\n")

    def log(self, message):
        """将日志消息记录到 log.md 文件中，使用 cmd 代码块"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write("```cmd\n")
                f.write(log_entry)
                f.write("```\n\n")
        except Exception as e:
            print(f"Failed to write to log file: {str(e)}")

    def connect(self):
        """连接到邮箱服务器"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_addr, self.password)
            self.mail.select('INBOX')
            self.log("Connected to the email server successfully.")
        except imaplib.IMAP4.error as e:
            self.log(f"Failed to connect to the email server: {str(e)}")
            exit(1)

    def get_emails(self):
        """获取邮件列表"""
        try:
            _, messages = self.mail.search(None, 'ALL')
            email_ids = messages[0].split()
            self.log(f"Found {len(email_ids)} emails.")
            return email_ids
        except Exception as e:
            self.log(f"Failed to retrieve emails: {str(e)}")
            return []

    def decode_str(self, s):
        """解码邮件主题"""
        try:
            value, charset = decode_header(s)[0]
            if charset:
                value = value.decode(charset)
            return value
        except Exception as e:
            self.log(f"Failed to decode string: {str(e)}")
            return "No Subject"

    def process_email(self, email_id):
        """处理单封邮件"""
        try:
            _, msg_data = self.mail.fetch(email_id, '(RFC822)')
            if not msg_data or not msg_data[0]:
                self.log(f"Failed to fetch email ID {email_id}")
                return None, None, []
            
            email_body = msg_data[0][1]
            message = email.message_from_bytes(email_body)
            
            # 获取邮件主题
            subject = self.decode_str(message.get('subject', 'No Subject'))
            
            # 处理邮件内容和附件
            content = []
            attachments = []
            
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                fileName = part.get_filename()
                if part.get_content_type() == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        content.append(payload.decode(charset))
                    except Exception as e:
                        self.log(f"Error decoding content for email ID {email_id}: {str(e)}")
                        content.append("Content decoding error")
                elif fileName:
                    attachments.append(part)
                    
            return subject, '\n'.join(content), attachments
        except Exception as e:
            self.log(f"Error processing email ID {email_id}: {str(e)}")
            return None, None, []

    def save_attachment(self, attachment):
        """保存图片附件"""
        filename = self.decode_str(attachment.get_filename())
        if filename:
            filepath = os.path.join(self.img_folder, filename)
            try:
                with open(filepath, 'wb') as f:
                    f.write(attachment.get_payload(decode=True))
                self.log(f"Saved attachment: {filepath}")
                return filepath
            except Exception as e:
                self.log(f"Failed to save attachment {filename}: {str(e)}")
        return None

    def delete_email(self, email_id):
        """处理完邮件后删除邮件"""
        try:
            self.mail.store(email_id, '+FLAGS', '\\Deleted')
            self.mail.expunge()
            self.log(f"Deleted email ID {email_id}.")
        except Exception as e:
            self.log(f"Failed to delete email ID {email_id}: {str(e)}")

    def append_to_markdown(self, subject, content, image_paths):
        """将内容追加到 Markdown 文件，并记录日志"""
        sanitized_subject = re.sub(r'[^\w\-_\s.]','', subject).lower().replace(' ', '-')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        try:
            with open(self.md_file, 'a', encoding='utf-8') as f:
                f.write(f'\n## {subject} ({current_time})\n\n')
                f.write(f'{content}\n\n')
                for img_path in image_paths:
                    if img_path:
                        relative_path = os.path.relpath(img_path, os.path.dirname(self.md_file))
                        f.write(f'![{sanitized_subject}-{os.path.splitext(os.path.basename(img_path))[0]}]({relative_path})\n\n')
            self.log(f"Appended email '{subject}' to {self.md_file}.")
        except Exception as e:
            self.log(f"Failed to append to Markdown file: {str(e)}")

    def run_upload_script(self):
        """运行同目录下的 upload.sh 脚本"""
        try:
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload.sh')
            if not os.path.exists(script_path):
                self.log(f"upload.sh not found at {script_path}.")
                return False
            subprocess.run(['bash', script_path], check=True)
            self.log("upload.sh executed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"upload.sh failed with error: {e}")
            return False
        except Exception as e:
            self.log(f"Failed to run upload.sh: {str(e)}")
            return False

    def process_all_emails(self):
        """循环处理所有邮件，并在处理每封邮件后运行 upload.sh"""
        self.connect()
        while True:
            email_ids = self.get_emails()
            if not email_ids:
                self.log("No new emails to process. Waiting for new emails...")
                time.sleep(3600)  # 每隔1小时检查一次
                continue
            
            for email_id in email_ids:
                subject, content, attachments = self.process_email(email_id)
                if subject is None:
                    continue
                image_paths = [self.save_attachment(att) for att in attachments]
                self.append_to_markdown(subject, content, image_paths)
                self.delete_email(email_id)
                
                # 运行 upload.sh
                self.run_upload_script()
                
                # 可选：等待一段时间，以避免过于频繁地运行脚本
                time.sleep(10)  # 等待10秒
                
        self.mail.close()
        self.mail.logout()

if __name__ == "__main__":
    EMAIL = "shihuaidexianyu@yeah.net"
    PASSWORD = "EPRk4j4StzAmFExj"
    IMAP_SERVER = "imap.yeah.net"
    MD_FILE = "output.md"

    processor = EmailProcessor(EMAIL, PASSWORD, IMAP_SERVER, MD_FILE)
    processor.process_all_emails()