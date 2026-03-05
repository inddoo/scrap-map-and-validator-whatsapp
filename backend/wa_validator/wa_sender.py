"""
WhatsApp Auto Sender
Mengirim pesan otomatis ke nomor WhatsApp yang sudah divalidasi
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import random


class WAAutoSender:
    """
    WhatsApp Auto Sender
    Mengirim pesan otomatis dengan delay untuk menghindari spam detection
    """
    
    def __init__(self, driver):
        """
        Initialize sender dengan driver yang sudah login
        
        Args:
            driver: Selenium WebDriver yang sudah login ke WhatsApp Web
        """
        self.driver = driver
        self.results = []
        
    def send_message(self, phone: str, message: str, delay: int = 3) -> Dict:
        """
        Kirim pesan ke satu nomor
        
        Args:
            phone: Nomor telepon (format: 628xxx)
            message: Pesan yang akan dikirim
            delay: Delay dalam detik sebelum kirim (default: 3)
            
        Returns:
            dict: Status pengiriman
        """
        result = {
            'phone': phone,
            'message_sent': False,
            'status': 'Pending...',
            'error': None
        }
        
        try:
            # Buka chat
            url = f'https://web.whatsapp.com/send?phone={phone}'
            print(f"  Opening chat: {phone}", flush=True)
            self.driver.get(url)
            
            # Tunggu halaman load
            time.sleep(5)
            
            # Cek apakah nomor valid (ada input box)
            input_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"][data-tab="6"]',
                'footer div[contenteditable="true"]',
                'div[data-testid="conversation-compose-box-input"]'
            ]
            
            input_box = None
            for selector in input_selectors:
                try:
                    input_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if input_box and input_box.is_displayed():
                        print(f"  ✓ Input box found", flush=True)
                        break
                except:
                    continue
            
            if not input_box:
                result['status'] = 'Nomor tidak valid atau tidak terdaftar'
                result['error'] = 'Input box not found'
                print(f"  ✗ Input box not found", flush=True)
                return result
            
            # Tunggu delay sebelum kirim (anti-spam)
            print(f"  Waiting {delay} seconds before sending...", flush=True)
            time.sleep(delay)
            
            # Ketik pesan (support multi-line dengan Shift+Enter)
            print(f"  Typing message...", flush=True)
            lines = message.split('\n')
            for i, line in enumerate(lines):
                input_box.send_keys(line)
                if i < len(lines) - 1:  # Jangan Shift+Enter di baris terakhir
                    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
            
            # Tunggu sebentar setelah ketik
            time.sleep(1)
            
            # Kirim pesan (Enter)
            print(f"  Sending message...", flush=True)
            input_box.send_keys(Keys.ENTER)
            
            # Tunggu pesan terkirim (lebih lama untuk memastikan)
            print(f"  Waiting for message to be sent...", flush=True)
            time.sleep(3)
            
            # Verifikasi pesan terkirim dengan multiple methods
            message_sent = False
            
            # Method 1: Cek apakah input box kosong (pesan sudah terkirim)
            try:
                current_text = input_box.text.strip()
                if not current_text or len(current_text) == 0:
                    message_sent = True
                    print(f"  ✓ Input box cleared - message sent", flush=True)
            except:
                pass
            
            # Method 2: Cek apakah ada pesan di chat (outgoing message)
            if not message_sent:
                try:
                    # Cek berbagai selector untuk pesan yang terkirim
                    message_selectors = [
                        'div[data-testid="msg-container"]',
                        'div.message-out',
                        'div[class*="message-out"]',
                        'span[data-testid="msg-dblcheck"]',  # Double check mark
                        'span[data-testid="msg-check"]'      # Single check mark
                    ]
                    
                    for selector in message_selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if len(elements) > 0:
                                message_sent = True
                                print(f"  ✓ Message found with selector: {selector}", flush=True)
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"  ⚠️ Error checking messages: {e}", flush=True)
            
            # Method 3: Cek apakah tidak ada error message
            if not message_sent:
                try:
                    error_indicators = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="alert-phone-unavailable"]')
                    if len(error_indicators) == 0:
                        # Tidak ada error, assume pesan terkirim
                        message_sent = True
                        print(f"  ✓ No error detected - assuming sent", flush=True)
                except:
                    pass
            
            # Set result
            if message_sent:
                result['message_sent'] = True
                result['status'] = '✓ Pesan terkirim'
                print(f"  ✓ Message sent successfully", flush=True)
            else:
                result['message_sent'] = False
                result['status'] = '⚠️ Status tidak pasti (mungkin terkirim)'
                print(f"  ⚠️ Cannot verify message status", flush=True)
            
        except Exception as e:
            result['status'] = f'Error: {str(e)}'
            result['error'] = str(e)
            print(f"  ✗ Error: {e}", flush=True)
            import traceback
            traceback.print_exc()
        
        return result
    
    def send_bulk_messages(
        self, 
        phone_numbers: List[str], 
        message: str,
        min_delay: int = 5,
        max_delay: int = 10,
        stop_on_error: bool = False
    ) -> List[Dict]:
        """
        Kirim pesan ke banyak nomor dengan delay random
        
        Args:
            phone_numbers: List nomor telepon
            message: Pesan yang akan dikirim (sama untuk semua)
            min_delay: Delay minimum antar pesan (detik)
            max_delay: Delay maximum antar pesan (detik)
            stop_on_error: Stop jika ada error (default: False)
            
        Returns:
            list: List hasil pengiriman
        """
        results = []
        total = len(phone_numbers)
        
        print(f"\n{'='*60}")
        print(f"SENDING MESSAGES TO {total} NUMBERS")
        print(f"{'='*60}\n")
        
        for idx, phone in enumerate(phone_numbers):
            print(f"[{idx+1}/{total}] Sending to: {phone}")
            
            # Random delay untuk menghindari detection
            delay = random.randint(min_delay, max_delay)
            
            result = self.send_message(phone, message, delay)
            results.append(result)
            
            print(f"  Status: {result['status']}\n")
            
            # Stop jika ada error dan stop_on_error = True
            if stop_on_error and result['error']:
                print(f"⚠️ Stopping due to error")
                break
            
            # Delay antar nomor (lebih lama)
            if idx < total - 1:
                wait_time = random.randint(min_delay + 2, max_delay + 5)
                print(f"  Waiting {wait_time} seconds before next message...\n")
                time.sleep(wait_time)
        
        self.results = results
        return results
    
    def send_personalized_messages(
        self,
        contacts: List[Dict],
        message_template: str,
        min_delay: int = 5,
        max_delay: int = 10
    ) -> List[Dict]:
        """
        Kirim pesan personal dengan template
        
        Args:
            contacts: List dict dengan 'phone' dan 'name' (atau field lain)
            message_template: Template pesan dengan placeholder {name}, {phone}, dll
            min_delay: Delay minimum antar pesan
            max_delay: Delay maximum antar pesan
            
        Returns:
            list: List hasil pengiriman
            
        Example:
            contacts = [
                {'phone': '628123456789', 'name': 'John'},
                {'phone': '628987654321', 'name': 'Jane'}
            ]
            template = "Halo {name}, ini pesan untuk Anda!"
        """
        results = []
        total = len(contacts)
        
        print(f"\n{'='*60}")
        print(f"SENDING PERSONALIZED MESSAGES TO {total} CONTACTS")
        print(f"{'='*60}\n")
        
        for idx, contact in enumerate(contacts):
            phone = contact.get('phone', '')
            
            # Format pesan dengan data contact
            try:
                personalized_message = message_template.format(**contact)
            except KeyError as e:
                print(f"⚠️ Warning: Template key {e} not found in contact data")
                personalized_message = message_template
            
            print(f"[{idx+1}/{total}] Sending to: {phone}")
            print(f"  Message: {personalized_message[:50]}...")
            
            delay = random.randint(min_delay, max_delay)
            result = self.send_message(phone, personalized_message, delay)
            result['contact'] = contact
            results.append(result)
            
            print(f"  Status: {result['status']}\n")
            
            # Delay antar nomor
            if idx < total - 1:
                wait_time = random.randint(min_delay + 2, max_delay + 5)
                print(f"  Waiting {wait_time} seconds before next message...\n")
                time.sleep(wait_time)
        
        self.results = results
        return results
    
    def get_summary(self) -> Dict:
        """
        Get summary statistik pengiriman
        
        Returns:
            dict: Summary dengan total, sent, failed
        """
        if not self.results:
            return {
                'total': 0,
                'sent': 0,
                'failed': 0,
                'sent_percent': 0,
                'failed_percent': 0
            }
        
        total = len(self.results)
        sent = sum(1 for r in self.results if r['message_sent'])
        failed = total - sent
        
        return {
            'total': total,
            'sent': sent,
            'failed': failed,
            'sent_percent': round(sent/total*100, 1) if total > 0 else 0,
            'failed_percent': round(failed/total*100, 1) if total > 0 else 0
        }


if __name__ == '__main__':
    """
    Test script
    """
    print("WhatsApp Auto Sender")
    print("=" * 60)
    print("This module requires an active WhatsApp Web session")
    print("Use with wa_checker.py driver instance")
    print("=" * 60)
