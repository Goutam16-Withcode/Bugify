from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class TestStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestCaseResult(BaseModel):
    name: str
    status: TestStatus
    duration: float = 0.0
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None


class TestSuiteResult(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration: float = 0.0
    cases: List[TestCaseResult] = Field(default_factory=list)
    raw_output: str = ""
    exit_code: int = 0


class VerificationVerdict(BaseModel):
    verified: bool
    reason: str
    test_suite_result: Optional[TestSuiteResult] = None
    regression_detected: bool = False
    syntax_error: Optional[str] = None
    applied_patch: Optional[str] = None


class SandboxExecutionResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    duration: float = 0.0
    timed_out: bool = False
    isolated: bool = True
