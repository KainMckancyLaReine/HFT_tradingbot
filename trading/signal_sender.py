import json
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SignalSender:
    def __init__(self, config):
        self.config = config
        
    def send_telegram_signal(self, signal):
        """
        Send signal via Telegram
        """
        if not self.config.get('telegram_enabled', False):
            return
            
        bot_token = self.config['telegram_bot_token']
        chat_id = self.config['telegram_chat_id']
        
        message = self.format_signal_message(signal)
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("✅ Telegram signal sent successfully")
            else:
                print(f"❌ Failed to send Telegram signal: {response.text}")
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    
    def send_email_signal(self, signal):
        """
        Send signal via email
        """
        if not self.config.get('email_enabled', False):
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg['Subject'] = f"Trading Signal: {signal['action']} XAU/USD"
            
            body = self.format_signal_message(signal, html=False)
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email_from'], self.config['email_password'])
            
            server.send_message(msg)
            server.quit()
            print("✅ Email signal sent successfully")
            
        except Exception as e:
            print(f"❌ Email error: {e}")
    
    def format_signal_message(self, signal, html=True):
        """
        Format signal message for sending
        """
        action_emoji = "🟢" if signal['action'] == 'BUY' else "🔴"
        
        if html:
            message = f"""
<b>{action_emoji} {signal['action']} SIGNAL - XAU/USD</b>

📅 <b>Date:</b> {signal['date']}
💰 <b>Price:</b> ${signal['price']:.2f}
📊 <b>Quantity:</b> {signal['quantity']}
📈 <b>RSI:</b> {signal.get('rsi', 'N/A')}
🎯 <b>Reason:</b> {signal['reason']}

{f"💵 <b>Profit:</b> {signal['profit_pct']:.2f}%" if 'profit_pct' in signal else ""}
            """
        else:
            message = f"""
{action_emoji} {signal['action']} SIGNAL - XAU/USD

Date: {signal['date']}
Price: ${signal['price']:.2f}
Quantity: {signal['quantity']}
RSI: {signal.get('rsi', 'N/A')}
Reason: {signal['reason']}

{f"Profit: {signal['profit_pct']:.2f}%" if 'profit_pct' in signal else ""}
            """
        
        return message.strip()