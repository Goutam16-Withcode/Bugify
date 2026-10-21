import re
from typing import Dict , Optional

class ErrorParser:
    
    def parse(self,traceback: str) -> Dict[str, Optional[str]]:
        if not traceback:
            return{
                "error_type":None,
                "error_message":None,
                "file" : None,
                "line" : None,
                "function":None,
            }
        
        error_type = None
        error_message = None
        file = None
        line = None
        function = None
        code_line = None
        
        match = re.search(r'File "(.+)", line (\d+), in (.+)', traceback)
        if match:
            file = match.group(1)
            line = match.group(2)
            function = match.group(3)

        # Look for the source line beneath File "...", line X, in Y
        line_match = re.search(r'File "[^"]+", line \d+, in [^\n]+\n\s+([^\n]+)', traceback)
        if line_match:
            code_line = line_match.group(1).strip()
        
        match = re.search(
            r'([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)):\s*(.+)',
            traceback
        )
        
        if match:
            error_type = match.group(1)
            error_message = match.group(2)
        
        return {
            "error_type": error_type,
            "error_message": error_message,
            "file": file,
            "line": line,
            "function": function,
            "code_line": code_line,
        }

    def parse_text(self, text: str) -> Dict[str, Optional[str]]:
        """Extract plausible error type and message from freeform text descriptions or logs."""
        if not text:
            return {"error_type": None, "error_message": None}

        m = re.search(r'\b([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception))\b', text)
        if m:
            return {"error_type": m.group(1), "error_message": text.strip()[:200]}

        t_lower = text.lower()
        if "divide by zero" in t_lower or "zero division" in t_lower:
            return {"error_type": "ZeroDivisionError", "error_message": "Division by zero"}
        if any(w in t_lower for w in ["payment", "gateway", "transaction", "divergence", "ledger", "charge"]):
            return {"error_type": "PaymentProcessingError", "error_message": "Payment gateway status validation failure"}
        if "keyerror" in t_lower or ("key" in t_lower and ("not found" in t_lower or "missing" in t_lower)):
            return {"error_type": "KeyError", "error_message": "Missing dictionary key"}
        if "attributeerror" in t_lower or "nonetype" in t_lower:
            return {"error_type": "AttributeError", "error_message": "NoneType has no attribute"}
        if "timeout" in t_lower:
            return {"error_type": "TimeoutError", "error_message": "Connection or execution timeout"}
        if "connection" in t_lower:
            return {"error_type": "ConnectionError", "error_message": "Connection failure"}

        return {"error_type": None, "error_message": None}