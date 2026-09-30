from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class BugSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BugCategory(str, Enum):
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGICAL = "logical"
    DEPENDENCY = "dependency"
    TYPE_ERROR = "type_error"
    RESOURCE_LEAK = "resource_leak"
    SECURITY = "security"
    PERFORMANCE = "performance"
    UNKNOWN = "unknown"


class ParsedError(BaseModel):
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    file: Optional[str] = None
    line: Optional[int] = None
    function: Optional[str] = None


class ClassificationResult(BaseModel):
    bug_type: Optional[str] = None
    category: BugCategory = BugCategory.UNKNOWN
    severity: BugSeverity = BugSeverity.MEDIUM
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class BugReport(BaseModel):
    problem: str = Field(..., description="High level problem description or bug title")
    traceback: str = Field(default="", description="Stack trace or error traceback")
    logs: str = Field(default="", description="Relevant runtime or build logs")
    repository_path: str = Field(..., description="Absolute or relative path to target repository")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DiagnosisResult(BaseModel):
    problem: str
    bug_type: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    confidence: float = 0.0
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    file: Optional[str] = None
    line: Optional[int] = None
    function: Optional[str] = None
    relevant_files: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    patterns: List[str] = Field(default_factory=list)
