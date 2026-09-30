from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentStep(BaseModel):
    agent_name: str
    action: str
    status: AgentStatus = AgentStatus.RUNNING
    details: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class AgentExecutionResult(BaseModel):
    agent_name: str
    success: bool
    output: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    duration: float = 0.0
