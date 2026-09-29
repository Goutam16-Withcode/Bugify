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
        
        match = re.search(r'File "(.+)", line (\d+), in (.+)', traceback)
        
        if match:
            file = match.group(1)
            line = match.group(2)
            function = match.group(3)
        
        match = re.search(
            r'([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)):\s*(.+)',
            traceback
        )
        
        if match:
            error_type = match.group(1)
            error_message = match.group(2)
        
        return{
            "error_type": error_type,
            "error_message": error_message,
            "file": file,
            "line": line,
            "function": function,
        }