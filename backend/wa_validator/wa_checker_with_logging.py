"""
WhatsApp Validator with File Logging
Untuk debug jika console output tidak muncul
"""
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wa_checker_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import original checker
from wa_validator.wa_checker import WAQueryChecker as OriginalChecker

class WAQueryChecker(OriginalChecker):
    """Wrapper with logging"""
    
    def login_whatsapp(self):
        logger.info("="*60)
        logger.info("MEMBUKA WHATSAPP WEB...")
        logger.info("="*60)
        
        result = super().login_whatsapp()
        
        logger.info(f"Login result: {result}")
        logger.info(f"is_logged_in: {self.is_logged_in}")
        logger.info(f"login_selector: {self.login_selector}")
        
        return result
    
    def validate_numbers(self, phone_numbers):
        logger.info(f"Validating {len(phone_numbers)} numbers...")
        logger.info(f"is_logged_in before validate: {self.is_logged_in}")
        
        result = super().validate_numbers(phone_numbers)
        
        logger.info(f"Validation complete. Results: {len(result)}")
        
        return result
