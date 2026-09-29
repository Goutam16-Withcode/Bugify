import re
from typing import Dict, List


class LogAnalyzer:

    def analyze(self, logs: str) -> Dict[str, List[str]]:
        if not logs:
            return {
                "errors": [],
                "warnings": [],
                "patterns": [],
            }

        errors = []
        warnings = []
        patterns = []

        for line in logs.splitlines():
            line = line.strip()

            if not line:
                continue

            # Error detection
            if re.search(
                r"(ERROR|EXCEPTION|FAILED|FAILURE|FATAL)",
                line,
                re.IGNORECASE,
            ):
                errors.append(line)

            # Warning detection
            if re.search(
                r"(WARNING|WARN|DEPRECATED)",
                line,
                re.IGNORECASE,
            ):
                warnings.append(line)

            # Common debugging patterns
            if re.search(
                r"(CUDA|OUT OF MEMORY|MEMORYERROR|TIMEOUT|"
                r"CONNECTION REFUSED|PERMISSION DENIED|"
                r"MODULE NOT FOUND|NOT FOUND|UNDEFINED)",
                line,
                re.IGNORECASE,
            ):
                patterns.append(line)

        return {
            "errors": errors,
            "warnings": warnings,
            "patterns": patterns,
        }