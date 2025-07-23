"""Input validation utilities."""

import re
from typing import Optional, Tuple


class Validator:
    """Input validation class."""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """Validate email format."""
        if not email.strip():
            return True, None  # Empty email is allowed
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, None
        else:
            return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
        """Validate phone number format."""
        if not phone.strip():
            return True, None  # Empty phone is allowed
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        if len(digits_only) >= 10:
            return True, None
        else:
            return False, "Phone number must contain at least 10 digits"
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """Validate name field."""
        name = name.strip()
        
        if not name:
            return False, "Name is required"
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        
        return True, None
    
    @staticmethod
    def validate_required_field(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """Validate required field."""
        if not value.strip():
            return False, f"{field_name} is required"
        return True, None
