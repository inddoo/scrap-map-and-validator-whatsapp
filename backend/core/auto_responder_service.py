"""
Persistent Auto Responder Service
Monitors WhatsApp Web for incoming messages and responds automatically using AI
"""
import time
import threading
from typing import Optional, Dict, List
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoResponderService:
    def __init__(self, driver, gemini_service):
        self.driver = driver
        self.gemini_service = gemini_service
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.response_prompt = "Anda adalah customer service yang ramah dan profesional. Jawab pertanyaan dengan sopan dan informatif."
        self.processed_messages: Dict[str, List[str]] = {}  # Track processed messages per chat
        self.check_interval = 1  # Check every 1 second for faster response!
        
    def start(self, response_prompt: Optional[str] = None, check_interval: Optional[int] = None):
        """Start the auto responder service
        
        Args:
            response_prompt: Custom prompt for AI responses
            check_interval: How often to check for new messages (in seconds). Default: 1 second for instant reply
        """
        if self.is_running:
            print("⚠️ Auto responder already running")
            return False
        
        # Verify driver is valid
        try:
            current_url = self.driver.current_url
            print(f"✓ Driver is valid, current URL: {current_url}")
            
            if 'web.whatsapp.com' not in current_url:
                print(f"⚠️ Warning: Not on WhatsApp Web! URL: {current_url}")
                print(f"   Auto responder may not work correctly.")
        except Exception as e:
            print(f"⚠️ Error checking driver: {e}")
            print(f"   Driver may not be initialized properly.")
            return False
        
        if response_prompt:
            self.response_prompt = response_prompt
        
        if check_interval is not None:
            self.check_interval = max(1, check_interval)  # Minimum 1 second
        
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
        print("✅ Auto responder started")
        print(f"   Prompt: {self.response_prompt[:50]}...")
        print(f"   Check interval: {self.check_interval} second(s) - {'⚡ INSTANT MODE' if self.check_interval <= 1 else 'Normal mode'}")
        return True
    
    def stop(self):
        """Stop the auto responder service"""
        if not self.is_running:
            print("⚠️ Auto responder not running")
            return False
        
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        
        print("✅ Auto responder stopped")
        return True
    
    def get_status(self) -> Dict:
        """Get current status of auto responder"""
        return {
            "is_running": self.is_running,
            "response_prompt": self.response_prompt,
            "check_interval": self.check_interval,
            "monitored_chats": len(self.processed_messages),
            "total_processed": sum(len(msgs) for msgs in self.processed_messages.values())
        }
    
    def update_prompt(self, new_prompt: str):
        """Update response prompt while running"""
        self.response_prompt = new_prompt
        print(f"✅ Prompt updated: {new_prompt[:50]}...")
    
    def _monitor_loop(self):
        """Main monitoring loop - runs in background thread"""
        print(f"🤖 Auto responder monitoring started")
        print(f"   Mode: INSTANT REPLY - Checking every {self.check_interval} second(s)")
        print(f"   Target: ONLY personal chats (NOT groups)")
        
        loop_count = 0
        
        while self.is_running:
            try:
                loop_count += 1
                
                # Only print every 10 loops to reduce spam
                if loop_count % 10 == 1:
                    print(f"\n[Loop #{loop_count}] Monitoring for new messages...")
                
                # Get all PERSONAL chats with unread messages (NOT groups)
                unread_chats = self._get_unread_chats()
                
                if unread_chats:
                    print(f"\n  ⚡ INSTANT: Found {len(unread_chats)} unread personal chat(s)!")
                
                for chat_info in unread_chats:
                    if not self.is_running:
                        break
                    
                    try:
                        print(f"\n  📱 Processing: {chat_info['name']} ({chat_info['phone']})")
                        
                        # Open chat
                        self._open_chat(chat_info)
                        time.sleep(0.5)  # Reduced wait time
                        
                        # Get ONLY the latest new incoming message
                        new_messages = self._get_new_messages(chat_info['phone'])
                        
                        if new_messages:
                            print(f"    ⚡ NEW MESSAGE detected!")
                        
                        # Process ONLY the first new message (latest)
                        if new_messages:
                            message = new_messages[0]
                            if not self.is_running:
                                break
                            
                            # Generate and send response IMMEDIATELY
                            self._handle_message(chat_info, message)
                            
                    except Exception as e:
                        print(f"⚠️ Error handling chat {chat_info.get('phone', 'unknown')}: {e}")
                        continue
                
                # Wait before next check (1 second for instant response)
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"⚠️ Error in monitor loop: {e}")
                time.sleep(self.check_interval)
        
        print("🤖 Auto responder monitoring stopped")
    
    def _get_unread_chats(self) -> List[Dict]:
        """Get list of chats with unread messages"""
        try:
            print(f"    Searching for chats...")
            
            # Strategy 1: Click "Belum dibaca" filter button first
            unread_chats = self._find_unread_chats_with_filter()
            if unread_chats:
                return unread_chats
            
            # Strategy 2: Try to find unread chats without filter
            unread_chats = self._find_unread_chats()
            if unread_chats:
                return unread_chats
            
            # Strategy 3: If no unread found, get all recent chats (top 10)
            print(f"      No unread chats found, checking recent chats...")
            return self._get_recent_chats()
            
        except Exception as e:
            print(f"⚠️ Error getting chats: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _find_unread_chats_with_filter(self) -> List[Dict]:
        """Click 'Belum dibaca' filter button and get unread chats from sidebar"""
        try:
            print(f"      Strategy: Using 'Belum dibaca' filter button...")
            
            # Step 1: Find and click "Belum dibaca" button
            unread_button_selectors = [
                '//span[contains(text(), "Belum dibaca")]',  # Indonesian
                '//span[contains(text(), "Unread")]',  # English
                '//div[contains(@aria-label, "Belum dibaca")]',
                '//div[contains(@aria-label, "Unread")]',
                '//button[contains(., "Belum dibaca")]',
                '//button[contains(., "Unread")]',
            ]
            
            button_clicked = False
            for selector in unread_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    for button in buttons:
                        if button.is_displayed():
                            # Check if button shows count (e.g., "Belum dibaca 1")
                            button_text = button.text
                            print(f"        Found filter button: {button_text}")
                            
                            # Click the button
                            try:
                                button.click()
                                button_clicked = True
                                print(f"        ✓ Clicked 'Belum dibaca' filter")
                                time.sleep(0.5)  # Wait for filter to apply
                                break
                            except:
                                # Try JavaScript click
                                self.driver.execute_script("arguments[0].click();", button)
                                button_clicked = True
                                print(f"        ✓ Clicked 'Belum dibaca' filter (JS)")
                                time.sleep(0.5)
                                break
                    
                    if button_clicked:
                        break
                except:
                    continue
            
            if not button_clicked:
                print(f"        ⚠️ 'Belum dibaca' button not found or not clickable")
                return []
            
            # Step 2: Now get chats from sidebar (should only show unread)
            print(f"        Getting chats from filtered list...")
            
            unread_chats = []
            
            # Get all visible chat items after filter
            chat_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            
            if not chat_items:
                chat_items = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            
            print(f"        Found {len(chat_items)} chat(s) in filtered list")
            
            for idx, chat_element in enumerate(chat_items[:10]):  # Max 10 unread chats
                try:
                    chat_text = chat_element.text.strip()
                    if not chat_text or len(chat_text) < 3:
                        continue
                    
                    lines = chat_text.split('\n')
                    chat_name = lines[0] if lines else 'Unknown'
                    
                    # Skip system messages
                    skip_keywords = ['Diarsipkan', 'Archived', 'Anda sekarang admin', 'pesan ini dihapus']
                    if any(kw in chat_text for kw in skip_keywords):
                        continue
                    
                    # SKIP GROUP CHATS
                    if self._is_group_chat(chat_element, chat_name):
                        print(f"        [{idx+1}] Skipping group: {chat_name}")
                        continue
                    
                    phone = self._extract_phone_from_chat(chat_element)
                    
                    chat_info = {
                        'element': chat_element,
                        'name': chat_name,
                        'phone': phone or chat_name
                    }
                    
                    print(f"        [{idx+1}] ✓ Found unread personal chat: {chat_name}")
                    unread_chats.append(chat_info)
                    
                except Exception as e:
                    continue
            
            # Step 3: Click "Semua" to reset filter
            try:
                semua_buttons = self.driver.find_elements(By.XPATH, '//span[contains(text(), "Semua")]')
                for btn in semua_buttons:
                    if btn.is_displayed():
                        try:
                            btn.click()
                            print(f"        ✓ Reset filter to 'Semua'")
                        except:
                            self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(0.3)
                        break
            except:
                pass
            
            if unread_chats:
                print(f"      ✓ Filter strategy found {len(unread_chats)} unread personal chat(s)")
            
            return unread_chats
            
        except Exception as e:
            print(f"      Filter strategy error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _find_unread_chats(self) -> List[Dict]:
        """Try to find chats with unread badge (ONLY personal chats, NOT groups)"""
        unread_chats = []
        
        # Strategy 1: Find by green circle with number (unread count badge)
        try:
            print(f"      Strategy 1: Looking for green unread count badges...")
            
            # The green circle with number - this is the most reliable indicator
            badge_selectors = [
                'span[data-icon="unread-count"]',  # Primary badge
                'div[aria-label*="unread"]',  # Aria label
                'span[aria-label*="unread"]',
                # Look for green background circle
                'span[style*="background"]',  # Badge usually has green background
            ]
            
            for selector in badge_selectors:
                try:
                    badge_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if badge_elements:
                        print(f"        Found {len(badge_elements)} badge(s) with {selector}")
                        
                        for badge in badge_elements:
                            try:
                                # Check if it's actually green (WhatsApp unread color)
                                bg_color = badge.value_of_css_property('background-color')
                                color = badge.value_of_css_property('color')
                                
                                # WhatsApp green: rgb(37, 211, 102) or similar
                                is_green = ('37, 211' in bg_color or '0, 168' in bg_color or 
                                           '37, 211' in color or '0, 168' in color)
                                
                                if not is_green and selector == 'span[style*="background"]':
                                    continue
                                
                                # Get parent chat element
                                chat_element = badge.find_element(By.XPATH, './ancestor::div[@role="listitem"]')
                                
                                # Extract chat info
                                chat_text = chat_element.text
                                lines = chat_text.split('\n')
                                chat_name = lines[0] if lines else 'Unknown'
                                
                                # SKIP GROUP CHATS
                                if self._is_group_chat(chat_element, chat_name):
                                    print(f"        Skipping group chat: {chat_name}")
                                    continue
                                
                                phone = self._extract_phone_from_chat(chat_element)
                                
                                chat_info = {
                                    'element': chat_element,
                                    'name': chat_name,
                                    'phone': phone or chat_name
                                }
                                
                                print(f"        ✓ Found unread personal chat: {chat_name}")
                                unread_chats.append(chat_info)
                                
                            except Exception as e:
                                continue
                        
                        if unread_chats:
                            break
                            
                except Exception as e:
                    continue
            
            if unread_chats:
                print(f"      ✓ Strategy 1 found {len(unread_chats)} unread chat(s)")
                return unread_chats
                
        except Exception as e:
            print(f"      Strategy 1 error: {e}")
        
        # Strategy 2: Find by green timestamp (like "21.07" in green)
        try:
            print(f"      Strategy 2: Looking for green timestamps...")
            
            # Get all chat list items
            chat_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            
            if not chat_items:
                chat_items = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            
            print(f"        Scanning {len(chat_items)} chat items...")
            
            for chat_element in chat_items:
                try:
                    # Look for green colored elements (timestamp or badge)
                    # WhatsApp green colors: rgb(0, 168, 132) or rgb(37, 211, 102)
                    green_elements = chat_element.find_elements(By.XPATH, 
                        './/*[contains(@style, "color: rgb(0, 168, 132)") or ' +
                        'contains(@style, "color: rgb(37, 211, 102)") or ' +
                        'contains(@style, "color:rgb(0,168,132)") or ' +
                        'contains(@style, "color:rgb(37,211,102)")]'
                    )
                    
                    # Also check for unread badge by data-icon
                    unread_badges = chat_element.find_elements(By.CSS_SELECTOR, 
                        'span[data-icon="unread-count"], span[data-testid="icon-unread"]'
                    )
                    
                    # Check for bold text (unread chats have bold names)
                    bold_elements = chat_element.find_elements(By.XPATH,
                        './/*[contains(@style, "font-weight: 700") or ' +
                        'contains(@style, "font-weight: bold") or ' +
                        'contains(@style, "font-weight:700") or ' +
                        'contains(@style, "font-weight:bold")]'
                    )
                    
                    # If any indicator found, this is unread
                    if green_elements or unread_badges or bold_elements:
                        chat_text = chat_element.text
                        lines = chat_text.split('\n')
                        chat_name = lines[0] if lines else 'Unknown'
                        
                        # Skip if too short
                        if len(chat_name) < 2:
                            continue
                        
                        # SKIP GROUP CHATS
                        if self._is_group_chat(chat_element, chat_name):
                            print(f"        Skipping group chat: {chat_name}")
                            continue
                        
                        phone = self._extract_phone_from_chat(chat_element)
                        
                        chat_info = {
                            'element': chat_element,
                            'name': chat_name,
                            'phone': phone or chat_name
                        }
                        
                        print(f"        ✓ Found unread personal chat: {chat_name} (green:{len(green_elements)}, badge:{len(unread_badges)}, bold:{len(bold_elements)})")
                        unread_chats.append(chat_info)
                        
                except Exception as e:
                    continue
            
            if unread_chats:
                print(f"      ✓ Strategy 2 found {len(unread_chats)} unread chat(s)")
                return unread_chats
                
        except Exception as e:
            print(f"      Strategy 2 error: {e}")
        
        # Strategy 3: Find by checking each chat's visual state
        try:
            print(f"      Strategy 3: Checking visual state of all chats...")
            
            # Get all chats
            all_chats = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            
            print(f"        Found {len(all_chats)} total chats")
            
            for idx, chat_element in enumerate(all_chats[:20]):  # Check first 20
                try:
                    # Get all span elements in this chat
                    spans = chat_element.find_elements(By.TAG_NAME, 'span')
                    
                    has_green = False
                    has_badge = False
                    
                    for span in spans:
                        # Check color
                        color = span.value_of_css_property('color')
                        bg_color = span.value_of_css_property('background-color')
                        
                        # Check if green
                        if ('37, 211' in color or '0, 168' in color or 
                            '37, 211' in bg_color or '0, 168' in bg_color):
                            has_green = True
                        
                        # Check if it's a badge (has number text and green background)
                        text = span.text.strip()
                        if text.isdigit() and '37, 211' in bg_color:
                            has_badge = True
                    
                    if has_green or has_badge:
                        chat_text = chat_element.text
                        lines = chat_text.split('\n')
                        chat_name = lines[0] if lines else 'Unknown'
                        
                        if len(chat_name) < 2:
                            continue
                        
                        # SKIP GROUP CHATS
                        if self._is_group_chat(chat_element, chat_name):
                            continue
                        
                        phone = self._extract_phone_from_chat(chat_element)
                        
                        chat_info = {
                            'element': chat_element,
                            'name': chat_name,
                            'phone': phone or chat_name
                        }
                        
                        print(f"        ✓ Found unread: {chat_name}")
                        unread_chats.append(chat_info)
                        
                except Exception as e:
                    continue
            
            if unread_chats:
                print(f"      ✓ Strategy 3 found {len(unread_chats)} unread chat(s)")
                return unread_chats
                
        except Exception as e:
            print(f"      Strategy 3 error: {e}")
        
        print(f"      ⚠️ No unread chats found with any strategy")
        return unread_chats
    
    def _get_recent_chats(self, limit: int = 10) -> List[Dict]:
        """Get recent chats (top N in chat list) - more aggressive search"""
        try:
            print(f"      Getting recent chats (limit: {limit})...")
            
            # First, verify we're on WhatsApp Web
            try:
                wa_indicators = [
                    'div[id="app"]',
                    'div[data-testid="conversation-panel-wrapper"]',
                    'header',
                ]
                
                found_wa = False
                for indicator in wa_indicators:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        found_wa = True
                        print(f"      ✓ WhatsApp Web detected (found {indicator})")
                        break
                
                if not found_wa:
                    print(f"      ⚠️ WhatsApp Web not detected!")
                    return []
                    
            except Exception as e:
                print(f"      ⚠️ Error checking WhatsApp state: {e}")
            
            recent_chats = []
            
            # Strategy 1: Find by role="listitem"
            try:
                print(f"      Strategy 1: Looking for div[role='listitem']...")
                chat_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
                print(f"        Found {len(chat_elements)} listitem(s)")
                
                if chat_elements:
                    for idx, chat_element in enumerate(chat_elements[:limit]):
                        try:
                            chat_text = chat_element.text.strip()
                            if not chat_text or len(chat_text) < 3:
                                continue
                            
                            lines = chat_text.split('\n')
                            chat_name = lines[0] if lines else 'Unknown'
                            
                            # Skip system messages
                            skip_keywords = ['Anda sekarang admin', 'Anda menghapus', 'pesan ini dihapus']
                            if any(kw in chat_name for kw in skip_keywords):
                                continue
                            
                            # SKIP GROUP CHATS
                            if self._is_group_chat(chat_element, chat_name):
                                print(f"        [{idx+1}] Skipping group: {chat_name}")
                                continue
                            
                            phone = self._extract_phone_from_chat(chat_element)
                            
                            chat_info = {
                                'element': chat_element,
                                'name': chat_name,
                                'phone': phone or chat_name
                            }
                            
                            print(f"        [{idx+1}] Found personal chat: {chat_name}")
                            recent_chats.append(chat_info)
                            
                        except Exception as e:
                            continue
                    
                    if recent_chats:
                        print(f"      ✓ Strategy 1 found {len(recent_chats)} personal chat(s)")
                        return recent_chats
            except Exception as e:
                print(f"      Strategy 1 error: {e}")
            
            # Strategy 2: Find by XPath - any div with chat-like structure
            try:
                print(f"      Strategy 2: Using XPath to find chats...")
                
                # Look for divs that contain both a name and a timestamp
                chat_elements = self.driver.find_elements(By.XPATH, 
                    '//div[contains(@class, "x10l6tqk") or contains(@class, "x1n2onr6")]//div[@role="listitem"]'
                )
                
                if not chat_elements:
                    # Alternative: Find any clickable chat-like elements
                    chat_elements = self.driver.find_elements(By.XPATH,
                        '//div[@role="listitem" and .//span[@dir="auto"]]'
                    )
                
                print(f"        Found {len(chat_elements)} chat element(s)")
                
                for idx, chat_element in enumerate(chat_elements[:limit]):
                    try:
                        chat_text = chat_element.text.strip()
                        if not chat_text or len(chat_text) < 3:
                            continue
                        
                        lines = chat_text.split('\n')
                        chat_name = lines[0] if lines else 'Unknown'
                        
                        # Skip system messages
                        skip_keywords = ['Anda sekarang admin', 'Anda menghapus', 'pesan ini dihapus']
                        if any(kw in chat_name for kw in skip_keywords):
                            continue
                        
                        # SKIP GROUP CHATS
                        if self._is_group_chat(chat_element, chat_name):
                            print(f"        [{idx+1}] Skipping group: {chat_name}")
                            continue
                        
                        phone = self._extract_phone_from_chat(chat_element)
                        
                        chat_info = {
                            'element': chat_element,
                            'name': chat_name,
                            'phone': phone or chat_name
                        }
                        
                        print(f"        [{idx+1}] Found personal chat: {chat_name}")
                        recent_chats.append(chat_info)
                        
                    except Exception as e:
                        continue
                
                if recent_chats:
                    print(f"      ✓ Strategy 2 found {len(recent_chats)} personal chat(s)")
                    return recent_chats
                    
            except Exception as e:
                print(f"      Strategy 2 error: {e}")
            
            print(f"      ⚠️ No personal chats found with any strategy")
            return []
            
        except Exception as e:
            print(f"      Error getting recent chats: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extract_phone_from_chat(self, chat_element) -> Optional[str]:
        """Extract phone number from chat element"""
        try:
            # Try to get phone from various attributes
            text = chat_element.text
            
            # Look for phone number pattern
            import re
            phone_pattern = r'(\+?62\d{9,13}|\d{10,13})'
            match = re.search(phone_pattern, text)
            
            if match:
                return match.group(1)
            
            return None
            
        except:
            return None
    
    def _is_group_chat(self, chat_element, chat_name: str) -> bool:
        """Detect if a chat is a group chat (return True for groups, False for personal chats)"""
        try:
            # Strategy 1: Check for group indicators in chat name
            group_keywords = [
                'GRUP', 'GROUP', 'KOMUNITAS', 'COMMUNITY', 
                'SOLUSI', 'KELUARGA', 'HARMONI', 'ADMIN',
                'TEAM', 'TIM', 'KELAS', 'CLASS'
            ]
            
            chat_name_upper = chat_name.upper()
            for keyword in group_keywords:
                if keyword in chat_name_upper:
                    return True
            
            # Strategy 2: Check for group icon
            try:
                # Group chats usually have a group icon
                group_icons = chat_element.find_elements(By.CSS_SELECTOR, 'span[data-icon="default-group"]')
                if group_icons:
                    return True
            except:
                pass
            
            # Strategy 3: Check aria-label for "grup" keyword
            try:
                aria_label = chat_element.get_attribute('aria-label') or ''
                if 'grup' in aria_label.lower() or 'group' in aria_label.lower():
                    return True
            except:
                pass
            
            # Strategy 4: Check if chat text contains multiple participant indicators
            try:
                text = chat_element.text
                # Group chats often show participant names like "Name: message"
                if ':' in text and len(text.split(':')) > 2:
                    return True
            except:
                pass
            
            return False
            
        except Exception as e:
            # If we can't determine, assume it's personal (safer to respond)
            return False
    
    def _open_chat(self, chat_info: Dict):
        """Open a specific chat"""
        try:
            chat_element = chat_info['element']
            chat_element.click()
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error opening chat: {e}")
    
    def _get_new_messages(self, chat_id: str) -> List[str]:
        """Get ONLY the latest NEW incoming message from current chat (messages TO you, not FROM you)"""
        try:
            # Initialize processed messages for this chat if not exists
            if chat_id not in self.processed_messages:
                self.processed_messages[chat_id] = []
            
            # Wait a bit for messages to load
            time.sleep(0.5)
            
            # Selectors for INCOMING messages only (from contact, not from us)
            # These are messages that came TO you
            incoming_selectors = [
                'div.message-in',  # Incoming message container
                'div[class*="message-in"]',  # Incoming message with class containing "message-in"
            ]
            
            new_messages = []
            
            for selector in incoming_selectors:
                try:
                    # Find all incoming message elements
                    message_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if not message_elements:
                        continue
                    
                    # Get ONLY the LAST incoming message (most recent)
                    # We only want to respond to the latest unread message
                    last_message = message_elements[-1]
                    
                    try:
                        # Get message text from the bubble
                        text_elements = last_message.find_elements(By.CSS_SELECTOR, 'span.selectable-text')
                        if not text_elements:
                            text_elements = last_message.find_elements(By.CSS_SELECTOR, 'span[dir="ltr"]')
                        
                        if text_elements:
                            message_text = text_elements[0].text.strip()
                        else:
                            message_text = last_message.text.strip()
                        
                        # Skip if empty
                        if not message_text or len(message_text) < 2:
                            continue
                        
                        # Skip if already processed
                        if message_text in self.processed_messages[chat_id]:
                            continue
                        
                        # Skip system messages
                        skip_keywords = [
                            'Pesan ini dihapus',
                            'Pesan dihapus',
                            'bergabung menggunakan',
                            'keluar',
                            'Anda menambahkan',
                            'Anda sekarang admin',
                            'menghapus pesan ini',
                            'Enkripsi end-to-end',
                        ]
                        
                        should_skip = False
                        for keyword in skip_keywords:
                            if keyword in message_text:
                                should_skip = True
                                break
                        
                        if should_skip:
                            continue
                        
                        # This is a new incoming message!
                        new_messages.append(message_text)
                        self.processed_messages[chat_id].append(message_text)
                        
                        # Only process ONE message at a time
                        break
                        
                    except Exception as e:
                        continue
                    
                    if new_messages:
                        break
                        
                except Exception as e:
                    continue
            
            return new_messages
            
        except Exception as e:
            print(f"⚠️ Error getting new messages: {e}")
            return []
    
    def _handle_message(self, chat_info: Dict, message: str):
        """Handle incoming message - generate and send response"""
        try:
            phone = chat_info['phone']
            name = chat_info['name']
            
            print(f"\n📨 New message from {name} ({phone})")
            print(f"   Message: {message[:50]}...")
            
            # Generate AI response
            sender_data = {
                'phone': phone,
                'name': name
            }
            
            ai_response = self.gemini_service.generate_auto_response(
                incoming_message=message,
                sender_data=sender_data,
                response_prompt=self.response_prompt,
                conversation_history=None
            )
            
            print(f"   🤖 AI Response: {ai_response[:50]}...")
            
            # Send response
            success = self._send_response(ai_response)
            
            if success:
                print(f"   ✅ Response sent successfully")
                
                # Mark our response as processed too (to avoid responding to our own messages)
                if phone in self.processed_messages:
                    self.processed_messages[phone].append(ai_response)
            else:
                print(f"   ❌ Failed to send response")
            
        except Exception as e:
            print(f"⚠️ Error handling message: {e}")
    
    def _send_response(self, message: str) -> bool:
        """Send response message"""
        try:
            from selenium.webdriver.common.keys import Keys
            
            # First, aggressively close any popups/dialogs that might be blocking
            try:
                # Try multiple times to close popups
                for attempt in range(3):
                    closed_something = False
                    
                    close_selectors = [
                        'button[aria-label="Tutup"]',
                        'button[aria-label="Close"]',
                        'div[role="button"][aria-label="Tutup"]',
                        'span[data-icon="x"]',
                        'span[data-icon="x-viewer"]',
                        'div[role="dialog"] button',
                    ]
                    
                    for selector in close_selectors:
                        try:
                            close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for btn in close_buttons:
                                if btn.is_displayed():
                                    btn.click()
                                    time.sleep(0.3)
                                    print(f"      Closed popup/dialog (attempt {attempt+1})")
                                    closed_something = True
                        except:
                            continue
                    
                    # Also try ESC key to close dialogs
                    try:
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(0.2)
                    except:
                        pass
                    
                    if not closed_something:
                        break
                        
            except Exception as e:
                print(f"      Warning closing popups: {e}")
            
            # Find CHAT input box (NOT search box!)
            # Must be in footer area and have correct aria-label
            print(f"      🔍 Looking for chat input box...")
            
            input_box = None
            
            # Strategy 1: Find by footer + aria-label
            try:
                footer = self.driver.find_element(By.CSS_SELECTOR, 'footer')
                input_candidates = footer.find_elements(By.CSS_SELECTOR, 'div[contenteditable="true"]')
                
                for elem in input_candidates:
                    if not elem.is_displayed() or not elem.is_enabled():
                        continue
                    
                    aria_label = elem.get_attribute('aria-label') or ''
                    
                    # Must contain "ketik pesan" or "type a message"
                    if 'ketik pesan' in aria_label.lower() or 'type a message' in aria_label.lower():
                        input_box = elem
                        print(f"      ✓ Found chat input: {aria_label[:60]}")
                        break
            except Exception as e:
                print(f"      ⚠️ Strategy 1 failed: {e}")
            
            # Strategy 2: Find by data-testid
            if not input_box:
                try:
                    input_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="conversation-compose-box-input"]')
                    if input_box.is_displayed() and input_box.is_enabled():
                        print(f"      ✓ Found chat input by testid")
                    else:
                        input_box = None
                except:
                    pass
            
            # Strategy 3: Find by data-tab in footer
            if not input_box:
                try:
                    input_box = self.driver.find_element(By.CSS_SELECTOR, 'footer div[contenteditable="true"][data-tab="10"]')
                    if input_box.is_displayed() and input_box.is_enabled():
                        print(f"      ✓ Found chat input by data-tab")
                    else:
                        input_box = None
                except:
                    pass
            
            if not input_box:
                print(f"      ❌ Could not find chat input box!")
                print(f"      Make sure a chat is open and input box is visible")
                return False
            
            # Sanitize message (remove emojis, BMP chars)
            sanitized_message = self._sanitize_message(message)
            
            # Scroll into view and focus using JavaScript
            try:
                self.driver.execute_script("""
                    arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});
                """, input_box)
                time.sleep(0.3)
                
                # Click using JavaScript to avoid interception
                self.driver.execute_script("arguments[0].click();", input_box)
                time.sleep(0.3)
                
                # Focus using JavaScript
                self.driver.execute_script("arguments[0].focus();", input_box)
                time.sleep(0.3)
                
            except Exception as e:
                print(f"      Warning during focus: {e}")
                # Fallback to regular click
                try:
                    input_box.click()
                    time.sleep(0.3)
                except:
                    pass
            
            # Type message line by line
            lines = sanitized_message.split('\n')
            for i, line in enumerate(lines):
                input_box.send_keys(line)
                if i < len(lines) - 1:
                    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
                    time.sleep(0.1)
            
            time.sleep(0.5)
            
            # Send
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error sending response: {e}")
            return False
    
    def _sanitize_message(self, message: str) -> str:
        """Remove characters outside BMP that ChromeDriver doesn't support"""
        import re
        
        # Remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002600-\U000026FF"
            "\U00002700-\U000027BF"
            "]+",
            flags=re.UNICODE
        )
        
        sanitized = emoji_pattern.sub('', message)
        
        # Filter characters outside BMP but preserve line breaks
        sanitized = ''.join(
            char for char in sanitized 
            if ord(char) <= 0xFFFF or char in ['\n', '\r', '\t']
        )
        
        # Clean up excessive spaces
        lines = sanitized.split('\n')
        cleaned_lines = [re.sub(r' +', ' ', line.strip()) for line in lines]
        sanitized = '\n'.join(cleaned_lines)
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
        
        return sanitized.strip()


# Global instance
_auto_responder_service: Optional[AutoResponderService] = None


def get_auto_responder_service(driver=None, gemini_service=None) -> Optional[AutoResponderService]:
    """Get or create auto responder service instance"""
    global _auto_responder_service
    
    if _auto_responder_service is None and driver and gemini_service:
        _auto_responder_service = AutoResponderService(driver, gemini_service)
    
    return _auto_responder_service


def reset_auto_responder_service():
    """Reset auto responder service (for cleanup)"""
    global _auto_responder_service
    
    if _auto_responder_service and _auto_responder_service.is_running:
        _auto_responder_service.stop()
    
    _auto_responder_service = None
