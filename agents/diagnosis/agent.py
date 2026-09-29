from typing import List , Dict , Optional
from agents.diagnosis.subagents.error_parser import ErrorParser
from agents.diagnosis.subagents.log_analyzer import LogAnalyzer
from agents.diagnosis.subagents.bug_classifier import BugClassifier

class DiagnosisAgent:
    
    def __init__(self):
        self.error_parser = ErrorParser()
        self.log_analyzer = LogAnalyzer()
        self.bug_classifier = BugClassifier()

    def analyze(
        self,
        problem : str,
        traceback : str,
        logs: str
    ) -> Dict : 
        
        parsed_error = self.error_parser.parse(traceback)
        log_analysis = self.log_analyzer.analyze(logs)
        classification = self.bug_classifier.classify(
            error_type=parsed_error.get("error_type"),
            error_message=parsed_error.get("error_message"),
            logs=log_analysis.get("logs", []),
            patterns=log_analysis.get("patterns", [])
        )
        
        relevant_files: List[str] = []

        if parsed_error.get("file"):
            relevant_files.append(parsed_error["file"])

        return {
            "problem": problem,
            "bug_type": classification.get("bug_type"),
            "category": classification.get("category"),
            "severity": classification.get("severity"),
            "confidence": classification.get("confidence"),

            "error_type": parsed_error.get("error_type"),
            "error_message": parsed_error.get("error_message"),
            "file": parsed_error.get("file"),
            "line": parsed_error.get("line"),
            "function": parsed_error.get("function"),

            "relevant_files": relevant_files,

            "errors": log_analysis.get("errors", []),
            "warnings": log_analysis.get("warnings", []),
            "patterns": log_analysis.get("patterns", []),
        }