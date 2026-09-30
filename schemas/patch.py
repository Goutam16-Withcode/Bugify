from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class ReviewDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"
    REJECT = "reject"


class PatchIssue(BaseModel):
    category: str
    message: str
    line: Optional[int] = None
    severity: str = "warning"


class PatchProposal(BaseModel):
    patch: str = Field(..., description="Unified diff text")
    summary: str = Field(default="", description="Summary of changes")
    target_files: List[str] = Field(default_factory=list)
    confidence: float = 0.0


class PatchReviewResult(BaseModel):
    decision: ReviewDecision
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = ""
    issues: List[PatchIssue] = Field(default_factory=list)
    syntax_valid: bool = True
    scope_valid: bool = True


class RefactoringResult(BaseModel):
    refactored_patch: str
    changes_made: List[str] = Field(default_factory=list)
    cleanliness_score: float = 1.0


class UnifiedDiff(BaseModel):
    filename: str
    original_code: Optional[str] = None
    modified_code: Optional[str] = None
    diff_text: str
