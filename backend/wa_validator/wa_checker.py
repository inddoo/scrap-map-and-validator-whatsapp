"""
WhatsApp Validator - Query Method
Menggunakan Store.QueryExist.queryExist untuk validasi cepat
Metode ini lebih cepat dan reliable karena langsung query ke server WhatsApp
"""
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import List, Dict
import json


class WAQueryChecker:
    """
    WhatsApp Validator menggunakan Store.QueryExist.queryExist
    Metode ini mengakses fungsi internal WhatsApp Web untuk query nomor
    """
    
    def __init__(self):
        self.driver = None
        self.results = []
        self.is_logged_in = False
        self.login_selector = None  # Store which selector worked
        
    def debug_page_elements(self):
        """Debug function to see what elements are available"""
        print("\n" + "="*60, flush=True)
        print("DEBUG: Checking page elements...", flush=True)
        print("="*60, flush=True)
        
        selectors_to_check = [
            'div[aria-label="Chat list"]',
            'div[aria-label="Daftar chat"]',
            'div[data-testid="chat-list"]',
            '#pane-side',
            'div[id="side"]',
            '#app',
            'div[data-testid="conversation-panel-wrapper"]'
        ]
        
        for selector in selectors_to_check:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✓ Found: {selector}", flush=True)
            except:
                print(f"✗ Not found: {selector}", flush=True)
        
        print("="*60 + "\n", flush=True)
        
    def setup_driver(self):
        """Setup Chrome dengan session save"""
        options = Options()
        
        # User data directory untuk save session
        user_data_dir = os.path.abspath('./wa_session')
        os.makedirs(user_data_dir, exist_ok=True)
        
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        # Anti-detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        print("✓ Chrome initialized")
        
    def login_whatsapp(self):
        """Login WhatsApp Web"""
        print("\n" + "="*60, flush=True)
        print("MEMBUKA WHATSAPP WEB...", flush=True)
        print("="*60, flush=True)
        
        try:
            print("Loading https://web.whatsapp.com ...", flush=True)
            self.driver.get('https://web.whatsapp.com')
            print("✓ Page loaded", flush=True)
        except Exception as e:
            print(f"✗ Error loading page: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return False
        
        print("Waiting 5 seconds...", flush=True)
        time.sleep(5)
        
        # Debug: Check what elements are available
        try:
            self.debug_page_elements()
        except Exception as e:
            print(f"Error in debug: {e}", flush=True)
        
        # Cek apakah sudah login dengan berbagai selector
        login_selectors = [
            'div[aria-label="Chat list"]',
            'div[aria-label="Daftar chat"]',
            'div[data-testid="chat-list"]',
            '#pane-side',
            'div[id="side"]'
        ]
        
        print("Checking if already logged in...", flush=True)
        is_already_logged_in = False
        for selector in login_selectors:
            try:
                print(f"  Trying selector: {selector}", flush=True)
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element:
                    print(f"✓ SUDAH LOGIN! (Detected with: {selector})", flush=True)
                    self.login_selector = selector  # Save working selector
                    is_already_logged_in = True
                    break
            except Exception as e:
                print(f"  ✗ Not found: {selector}", flush=True)
                continue
        
        if is_already_logged_in:
            self.is_logged_in = True
            
            # Tunggu sebentar untuk memastikan fully loaded
            print("Menunggu WhatsApp Web fully loaded...", flush=True)
            time.sleep(5)
            
            print("✓ WhatsApp Web ready!", flush=True)
            return True
        
        # Belum login - perlu scan QR
        print("\n" + "="*60, flush=True)
        print("⚠️  SCAN QR CODE SEKARANG!", flush=True)
        print("="*60, flush=True)
        print("Di HP Anda:", flush=True)
        print("1. Buka WhatsApp", flush=True)
        print("2. Tap Menu (⋮) > Linked Devices", flush=True)
        print("3. Tap 'Link a Device'", flush=True)
        print("4. Scan QR di Chrome", flush=True)
        print("="*60, flush=True)
        print("\nMenunggu scan... (120 detik)", flush=True)
        
        # Tunggu sampai login berhasil
        login_success = False
        for selector in login_selectors:
            try:
                print(f"  Waiting for selector: {selector}", flush=True)
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"\n✓ Login berhasil! (Detected with: {selector})", flush=True)
                self.login_selector = selector  # Save working selector
                login_success = True
                break
            except Exception as e:
                print(f"  ✗ Timeout for: {selector}", flush=True)
                continue
        
        if not login_success:
            print("\n✗ Timeout - tidak ada selector yang terdeteksi", flush=True)
            print("Checking page again...", flush=True)
            try:
                self.debug_page_elements()
            except:
                pass
            return False
        
        print("✓ Session tersimpan!", flush=True)
        self.is_logged_in = True
        
        # Tunggu lebih lama untuk memastikan WhatsApp Web fully loaded
        print("Menunggu WhatsApp Web fully loaded...", flush=True)
        time.sleep(10)
        
        # Verify login dengan cek lagi
        print("Verifying login...", flush=True)
        verified = False
        for selector in login_selectors:
            try:
                self.driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✓ Verified with: {selector}", flush=True)
                verified = True
                break
            except:
                continue
        
        if verified:
            print("✓ WhatsApp Web ready!", flush=True)
            return True
        else:
            print("⚠️ Warning: Could not verify login", flush=True)
            print("Checking page again...", flush=True)
            try:
                self.debug_page_elements()
            except:
                pass
            return True  # Return True anyway, mungkin selector berubah
    
    def wait_for_whatsapp_ready(self):
        """Tunggu sampai WhatsApp Web fully loaded"""
        print("Waiting for WhatsApp Web to be ready...", flush=True)
        
        # Tunggu halaman fully loaded
        print("Waiting for page to be fully loaded...", flush=True)
        time.sleep(5)
        
        # Langsung inject Store script
        print("Injecting Store exposure script...", flush=True)
        try:
            self.inject_store_script()
            print("✓ Store injection script executed", flush=True)
        except Exception as e:
            print(f"✗ Error injecting Store: {e}", flush=True)
        
        # Tunggu sebentar
        time.sleep(3)
        
        # Cek apakah Store tersedia
        for attempt in range(10):
            try:
                result = self.driver.execute_script("""
                    return typeof window.Store !== 'undefined' && 
                           typeof window.Store.QueryExist !== 'undefined';
                """)
                if result:
                    print(f"✓ WhatsApp Store ready! (attempt {attempt + 1})", flush=True)
                    return True
            except Exception as e:
                print(f"  Attempt {attempt + 1}: Store not ready yet", flush=True)
            
            time.sleep(2)
        
        # Last attempt - cek Store saja (tanpa QueryExist)
        try:
            result = self.driver.execute_script("""
                return typeof window.Store !== 'undefined';
            """)
            if result:
                print("✓ Store available (QueryExist might not be available)", flush=True)
                return True
        except:
            pass
        
        print("✗ Failed to access WhatsApp Store", flush=True)
        print("Trying alternative method...", flush=True)
        
        # Alternative: Cek apakah bisa akses window object
        try:
            result = self.driver.execute_script("return typeof window !== 'undefined';")
            if result:
                print("✓ Window object accessible", flush=True)
                # Force return True, kita coba query anyway
                return True
        except:
            pass
        
        return False
    
    def inject_store_script(self):
        """Inject script untuk expose WhatsApp Store object"""
        script = """
        (function() {
            if (window.Store) return;
            
            function getStore(modules) {
                let foundCount = 0;
                let neededObjects = [
                    { id: "Store", conditions: (module) => (module.default && module.default.Chat && module.default.Msg) ? module.default : null },
                    { id: "MediaCollection", conditions: (module) => (module.default && module.default.prototype && module.default.prototype.processFiles !== undefined) ? module.default : null },
                    { id: "MediaProcess", conditions: (module) => (module.BLOB) ? module : null },
                    { id: "Archive", conditions: (module) => (module.setArchive) ? module : null },
                    { id: "Block", conditions: (module) => (module.blockContact && module.unblockContact) ? module : null },
                    { id: "ChatUtil", conditions: (module) => (module.sendClear) ? module : null },
                    { id: "GroupInvite", conditions: (module) => (module.sendQueryGroupInviteCode) ? module : null },
                    { id: "Wap", conditions: (module) => (module.createGroup) ? module : null },
                    { id: "ServiceWorker", conditions: (module) => (module.default && module.default.killServiceWorker) ? module : null },
                    { id: "State", conditions: (module) => (module.STATE && module.STREAM) ? module : null },
                    { id: "WapDelete", conditions: (module) => (module.sendConversationDelete && module.sendConversationDelete.length == 2) ? module : null },
                    { id: "Conn", conditions: (module) => (module.default && module.default.ref && module.default.refTTL) ? module.default : null },
                    { id: "WapQuery", conditions: (module) => (module.queryExist) ? module : ((module.default && module.default.queryExist) ? module.default : null) },
                    { id: "CryptoLib", conditions: (module) => (module.decryptE2EMedia) ? module : null },
                    { id: "OpenChat", conditions: (module) => (module.default && module.default.prototype && module.default.prototype.openChat) ? module.default : null },
                    { id: "UserConstructor", conditions: (module) => (module.default && module.default.prototype && module.default.prototype.isServer && module.default.prototype.isUser) ? module.default : null },
                    { id: "SendTextMsgToChat", conditions: (module) => (module.sendTextMsgToChat) ? module.sendTextMsgToChat : null },
                    { id: "SendSeen", conditions: (module) => (module.sendSeen) ? module.sendSeen : null },
                    { id: "sendDelete", conditions: (module) => (module.sendDelete) ? module.sendDelete : null },
                    { id: "QueryExist", conditions: (module) => (module.queryWidExists || module.queryExist) ? module : null }
                ];
                
                for (let idx in modules) {
                    if ((typeof modules[idx] === "object") && (modules[idx] !== null)) {
                        neededObjects.forEach((needObj) => {
                            if (!needObj.conditions || needObj.foundedModule) return;
                            let neededModule = needObj.conditions(modules[idx]);
                            if (neededModule !== null) {
                                foundCount++;
                                needObj.foundedModule = neededModule;
                            }
                        });
                        
                        if (foundCount == neededObjects.length) {
                            break;
                        }
                    }
                }
                
                let neededStore = neededObjects.find((needObj) => needObj.id === "Store");
                window.Store = neededStore.foundedModule ? neededStore.foundedModule : {};
                neededObjects.splice(neededObjects.indexOf(neededStore), 1);
                neededObjects.forEach((needObj) => {
                    if (needObj.foundedModule) {
                        window.Store[needObj.id] = needObj.foundedModule;
                    }
                });
                
                window.Store.QueryExist = window.Store.QueryExist || window.Store.WapQuery;
                
                return window.Store;
            }
            
            if (typeof webpackChunkwhatsapp_web_client !== 'undefined') {
                webpackChunkwhatsapp_web_client.push([
                    ['parasite'],
                    {},
                    function(e) {
                        let modules = [];
                        for (let idx in e.m) {
                            modules.push(e(idx));
                        }
                        getStore(modules);
                    }
                ]);
            }
        })();
        """
        
        try:
            self.driver.execute_script(script)
            print("✓ Store injection script executed", flush=True)
        except Exception as e:
            print(f"✗ Store injection failed: {e}", flush=True)
    
    def clean_phone_number(self, phone: str) -> str:
        """
        Clean dan format nomor telepon
        User input angka setelah +62, sistem otomatis tambah 62 di depan
        """
        # Remove all non-digit characters
        phone = re.sub(r'\D', '', str(phone))
        
        # Remove leading 0 if exists
        if phone.startswith('0'):
            phone = phone[1:]  # 0812 → 812
        
        # Auto add 62 country code (user hanya input angka setelah +62)
        if not phone.startswith('62'):
            phone = '62' + phone  # 812 → 62812
        
        return phone
    
    def query_number(self, phone: str) -> Dict:
        """
        Query nomor menggunakan Store.QueryExist.queryExist
        Jika Store tidak tersedia, gunakan metode alternatif (open chat URL)
        """
        clean_phone = self.clean_phone_number(phone)
        
        result = {
            'phone': phone,
            'clean_phone': clean_phone,
            'has_whatsapp': False,
            'is_business': False,
            'business_name': '',
            'status': 'Checking...'
        }
        
        try:
            # Format nomor untuk WhatsApp (dengan @c.us)
            wid = f"{clean_phone}@c.us"
            
            print(f"  Querying: {clean_phone}", flush=True)
            
            # Try Store.QueryExist first
            query_script = f"""
            return new Promise((resolve) => {{
                try {{
                    if (!window.Store || !window.Store.QueryExist) {{
                        resolve({{ error: 'Store not available' }});
                        return;
                    }}
                    
                    window.Store.QueryExist.queryExist('{wid}').then((result) => {{
                        resolve({{
                            success: true,
                            wid: result.wid,
                            status: result.status,
                            isBusiness: result.biz || false,
                            businessName: result.vname || ''
                        }});
                    }}).catch((err) => {{
                        resolve({{ error: err.toString() }});
                    }});
                }} catch(e) {{
                    resolve({{ error: e.toString() }});
                }}
            }});
            """
            
            query_result = self.driver.execute_script(query_script)
            
            # If Store method failed, use alternative method
            if query_result.get('error'):
                print(f"  → Store method failed: {query_result['error']}", flush=True)
                print(f"  → Using alternative method (open chat URL)...", flush=True)
                return self.query_number_alternative(phone)
            
            # Parse hasil query
            if query_result.get('success'):
                status_code = query_result.get('status', 0)
                
                # Status 200 = nomor terdaftar WhatsApp
                if status_code == 200:
                    result['has_whatsapp'] = True
                    result['is_business'] = query_result.get('isBusiness', False)
                    result['business_name'] = query_result.get('businessName', '')
                    
                    if result['is_business']:
                        print(f"  → ✅ WhatsApp Business", flush=True)
                        if result['business_name']:
                            print(f"  → Name: {result['business_name']}", flush=True)
                            result['status'] = f"✓ WhatsApp Business - {result['business_name']}"
                        else:
                            result['status'] = "✓ WhatsApp Business"
                    else:
                        print(f"  → ✅ WhatsApp Personal", flush=True)
                        result['status'] = "✓ WhatsApp Personal"
                else:
                    # Status selain 200 = tidak terdaftar
                    print(f"  → ❌ Tidak terdaftar (status: {status_code})", flush=True)
                    result['status'] = f"Nomor tidak terdaftar WhatsApp"
            else:
                print(f"  → ⚠️ Query failed", flush=True)
                result['status'] = "Query failed"
                
        except Exception as e:
            print(f"  → Error: {e}", flush=True)
            result['status'] = f"Error: {str(e)}"
        
        return result
    
    def query_number_alternative(self, phone: str) -> Dict:
        """
        Metode alternatif: Buka chat URL dan cek apakah berhasil
        Tidak perlu Store.QueryExist
        """
        clean_phone = self.clean_phone_number(phone)
        
        result = {
            'phone': phone,
            'clean_phone': clean_phone,
            'has_whatsapp': False,
            'is_business': False,
            'business_name': '',
            'status': 'Checking...'
        }
        
        try:
            url = f'https://web.whatsapp.com/send?phone={clean_phone}'
            print(f"  Opening: {url}", flush=True)
            self.driver.get(url)
            
            # Wait for page load
            print(f"  Waiting 12 seconds for page load...", flush=True)
            time.sleep(12)
            
            print(f"  Page loaded, analyzing...", flush=True)
            
            # Get current URL and page source
            current_url = self.driver.current_url
            print(f"  Current URL: {current_url}", flush=True)
            
            page_source = self.driver.page_source.lower()
            current_url_lower = current_url.lower()
            
            # PRIORITY 1: Check for explicit error messages (HIGHEST PRIORITY)
            error_indicators = [
                'phone number shared via url is invalid',
                'nomor telepon yang dibagikan melalui url tidak valid',
                'tidak terdaftar di whatsapp',
                'tidak terdaftar pada whatsapp',
                'not registered on whatsapp',
                'invalid phone number',
                'número de teléfono no válido',
                'nao esta registrado no whatsapp',
                'is not registered',
                'tidak terdaftar'
            ]
            
            has_explicit_error = any(indicator in page_source for indicator in error_indicators)
            
            # Also check for error dialog/popup
            if not has_explicit_error:
                try:
                    # Check for dialog with error message
                    dialog_selectors = [
                        'div[role="dialog"]',
                        'div[data-testid="popup-contents"]',
                        'div.popup-contents',
                        'div[class*="popup"]',
                        'div[class*="dialog"]'
                    ]
                    
                    for selector in dialog_selectors:
                        try:
                            dialog = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if dialog and dialog.is_displayed():
                                dialog_text = dialog.text.lower()
                                if any(indicator in dialog_text for indicator in error_indicators):
                                    print(f"  → PRIORITY 1: Error dialog found ✗", flush=True)
                                    print(f"     Dialog text: {dialog_text[:100]}", flush=True)
                                    has_explicit_error = True
                                    break
                        except:
                            continue
                except Exception as e:
                    pass
            
            if has_explicit_error:
                print(f"  → PRIORITY 1: Explicit error found ✗", flush=True)
                result['has_whatsapp'] = False
                result['status'] = 'Nomor tidak terdaftar WhatsApp'
                return result
            else:
                print(f"  → PRIORITY 1: No explicit error ✓", flush=True)
            
            # PRIORITY 2: Check for message input box (STRONG INDICATOR)
            input_found = False
            input_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"][data-tab="6"]',
                'div[contenteditable="true"][data-tab="1"]',
                'footer div[contenteditable="true"]',
                'div[data-testid="conversation-compose-box-input"]',
                'div[role="textbox"][contenteditable="true"]',
                'div.copyable-text[contenteditable="true"]'
            ]
            
            print(f"  → Trying to find input box with {len(input_selectors)} selectors...", flush=True)
            
            for selector in input_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        # Check if visible and actually an input
                        if element.is_displayed() and element.get_attribute('contenteditable') == 'true':
                            print(f"  → PRIORITY 2: Input box found ({selector}) ✓", flush=True)
                            input_found = True
                            result['has_whatsapp'] = True
                            break
                except Exception as e:
                    continue
            
            if not input_found:
                print(f"  → PRIORITY 2: No input box found ✗", flush=True)
                
                # Save screenshot and HTML for debugging
                try:
                    screenshot_path = f"debug_wa_{clean_phone}.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"  → Screenshot saved: {screenshot_path}", flush=True)
                    
                    html_path = f"debug_wa_{clean_phone}.html"
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    print(f"  → HTML saved: {html_path}", flush=True)
                except:
                    pass
            
            # PRIORITY 3: Check for chat header (MEDIUM INDICATOR)
            header_found = False
            if not result['has_whatsapp']:
                header_selectors = [
                    'header[data-testid="conversation-header"]',
                    'div[data-testid="chat-header"]',
                    'div[data-testid="conversation-info-header"]'
                ]
                
                print(f"  → Trying to find chat header with {len(header_selectors)} selectors...", flush=True)
                
                for selector in header_selectors:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if element and element.is_displayed():
                            # Additional check: header should contain meaningful text
                            header_text = element.text.strip()
                            if len(header_text) > 3:  # Must have some text
                                print(f"  → PRIORITY 3: Chat header found ({selector}) ✓", flush=True)
                                print(f"     Header text: {header_text[:50]}...", flush=True)
                                header_found = True
                                result['has_whatsapp'] = True
                                break
                    except:
                        continue
                
                if not header_found:
                    print(f"  → PRIORITY 3: No chat header found ✗", flush=True)
            
            # PRIORITY 4: Check if URL changed (WEAK INDICATOR - only if above methods found nothing)
            if not result['has_whatsapp']:
                if 'send?phone' not in current_url_lower:
                    print(f"  → PRIORITY 4: URL changed from send page ✓", flush=True)
                    
                    # URL changed but no input/header found
                    # This is NOT enough to confirm valid number
                    # We MUST find input box or header
                    print(f"  → But no input box or header found, uncertain", flush=True)
                    print(f"  → ❌ Tidak terdaftar WhatsApp", flush=True)
                    result['has_whatsapp'] = False
                    result['status'] = 'Nomor tidak terdaftar WhatsApp'
                    return result
                else:
                    print(f"  → PRIORITY 4: Still on send page ✗", flush=True)
            
            # Final check - MUST have found input box or header
            if not result['has_whatsapp']:
                print(f"  → ❌ Tidak terdaftar WhatsApp", flush=True)
                result['status'] = 'Nomor tidak terdaftar WhatsApp'
                return result
            
            print(f"  → ✅ Terdaftar WhatsApp", flush=True)
            
            # Check for business indicators - SIMPLIFIED (only working methods)
            print(f"  Checking business indicators...", flush=True)
            time.sleep(2)
            
            business_indicators = []
            
            # PRIMARY METHOD: Check for catalog/storefront icon (MOST RELIABLE)
            print(f"  → Checking for catalog/storefront icon...", flush=True)
            
            catalog_selectors = [
                'span[data-icon="storefront"]',  # This one works!
                'span[data-icon="catalog"]',
                'span[data-icon="shop"]',
                'svg[data-icon="storefront"]',
                'button[aria-label*="Catalog"]',
                'button[aria-label*="Katalog"]'
            ]
            
            for selector in catalog_selectors:
                try:
                    catalog = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if catalog and catalog.is_displayed():
                        business_indicators.append(f'catalog:{selector}')
                        print(f"  → ✓ Catalog/storefront icon found", flush=True)
                        break
                except:
                    continue
            
            # SECONDARY METHOD: Check for verified badge
            try:
                verified_badge = self.driver.find_element(By.CSS_SELECTOR, 'span[data-icon="verified"]')
                if verified_badge and verified_badge.is_displayed():
                    business_indicators.append('verified-badge')
                    print(f"  → ✓ Verified badge found", flush=True)
            except:
                pass
            
            # Decision
            if len(business_indicators) > 0:
                result['is_business'] = True
                print(f"  → 💼 WhatsApp Business", flush=True)
            else:
                result['is_business'] = False
                print(f"  → 👤 WhatsApp Personal", flush=True)
            
            # Try to get name from header
            try:
                name_selectors = [
                    'header span[dir="auto"]',
                    'header [title]',
                    'div[data-testid="conversation-header"] span'
                ]
                for sel in name_selectors:
                    try:
                        elems = self.driver.find_elements(By.CSS_SELECTOR, sel)
                        for elem in elems:
                            text = elem.text.strip()
                            if text and 3 < len(text) < 100 and text != clean_phone:
                                result['business_name'] = text
                                print(f"  → Name: {text}", flush=True)
                                break
                        if result['business_name']:
                            break
                    except:
                        pass
            except Exception as e:
                print(f"  → Could not get name: {e}", flush=True)
            
            # Set status
            if result['is_business']:
                result['status'] = f"✓ WhatsApp Business{' - ' + result['business_name'] if result['business_name'] else ''}"
            else:
                result['status'] = f"WhatsApp Personal{' - ' + result['business_name'] if result['business_name'] else ''}"
                    
        except Exception as e:
            print(f"  → Error: {e}", flush=True)
            import traceback
            traceback.print_exc()
            result['status'] = f"Error: {str(e)}"
        
        return result
    
    def validate_numbers(self, phone_numbers: List[str]) -> List[Dict]:
        """Validasi multiple nomor"""
        # Re-check login status
        if not self.driver:
            print("Error: Driver not initialized!")
            return []
        
        # Cek apakah masih login dengan berbagai selector
        login_selectors = [
            'div[aria-label="Chat list"]',
            'div[aria-label="Daftar chat"]',
            'div[data-testid="chat-list"]',
            '#pane-side',
            'div[id="side"]'
        ]
        
        # Prioritaskan selector yang sudah berhasil sebelumnya
        if self.login_selector:
            login_selectors.insert(0, self.login_selector)
        
        is_logged_in = False
        for selector in login_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element:
                    print(f"✓ Login status verified (selector: {selector})")
                    is_logged_in = True
                    self.is_logged_in = True
                    break
            except:
                continue
        
        if not is_logged_in:
            print("Error: Not logged in! Please call login_whatsapp() first.")
            print("Tried selectors:", login_selectors)
            self.is_logged_in = False
            return []
        
        # Pastikan WhatsApp Web ready
        if not self.wait_for_whatsapp_ready():
            print("Error: WhatsApp Web not ready!")
            return []
        
        results = []
        total = len(phone_numbers)
        
        print(f"\n{'='*60}")
        print(f"VALIDATING {total} NUMBERS")
        print(f"{'='*60}\n")
        
        for idx, phone in enumerate(phone_numbers):
            if not phone or str(phone).strip() == '':
                continue
            
            print(f"[{idx+1}/{total}] {phone}")
            result = self.query_number(phone)
            results.append(result)
            print(f"  Status: {result['status']}\n")
            
            # Delay kecil antar query (1-2 detik cukup)
            if idx < total - 1:
                time.sleep(1.5)
        
        self.results = results
        return results
    
    def get_summary(self) -> Dict:
        """Get summary statistik"""
        if not self.results:
            return {
                'total': 0,
                'has_whatsapp': 0,
                'is_business': 0
            }
        
        total = len(self.results)
        has_wa = sum(1 for r in self.results if r['has_whatsapp'])
        is_business = sum(1 for r in self.results if r['is_business'])
        
        return {
            'total': total,
            'has_whatsapp': has_wa,
            'has_whatsapp_percent': round(has_wa/total*100, 1) if total > 0 else 0,
            'is_business': is_business,
            'is_business_percent': round(is_business/total*100, 1) if total > 0 else 0
        }
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("\nBrowser closed")


if __name__ == '__main__':
    import sys
    
    print("="*60)
    print("WHATSAPP VALIDATOR")
    print("="*60)
    
    # Test numbers (format: angka setelah +62)
    test_numbers = [
        '81234567890',
        '81111111111',
        '82222222222'
    ]
    
    checker = WAQueryChecker()
    
    try:
        checker.setup_driver()
        
        if not checker.login_whatsapp():
            print("Login failed")
            sys.exit(1)
        
        results = checker.validate_numbers(test_numbers)
        
        # Print summary
        summary = checker.get_summary()
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total: {summary['total']}")
        print(f"Has WhatsApp: {summary['has_whatsapp']} ({summary['has_whatsapp_percent']}%)")
        print(f"Business: {summary['is_business']} ({summary['is_business_percent']}%)")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        checker.close()
