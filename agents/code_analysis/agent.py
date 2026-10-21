from typing import Dict

from agents.code_analysis.subagents.repository_explorer import (
    RepositoryExplorer,
)

from agents.code_analysis.subagents.ast_analyzer import (
    ASTAnalyzer,
)

from agents.code_analysis.subagents.dependency_analyzer import (
    DependencyAnalyzer,
)


class CodeAnalysisAgent:
    """
    Main Code Analysis Agent.

    Combines:
    - Repository Explorer
    - AST Analyzer
    - Dependency Analyzer
    """

    def __init__(self):
        self.repository_explorer = RepositoryExplorer()
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()

    def analyze(
        self,
        repository_path: str,
        relevant_files: list[str] | None = None,
    ) -> Dict:
        """
        Perform complete repository and code analysis.

        Args:
            repository_path:
                Path to the target repository.

            relevant_files:
                Optional list of files identified by the
                Diagnosis Agent.

        Returns:
            Unified code analysis result.
        """

        # --------------------------------------------------
        # 1. Explore repository
        # --------------------------------------------------

        repository = self.repository_explorer.explore(
            repository_path
        )

        # --------------------------------------------------
        # 2. Analyze dependencies
        # --------------------------------------------------

        dependencies = self.dependency_analyzer.analyze(
            repository_path
        )

        # --------------------------------------------------
        # 3. Determine files for AST analysis
        # --------------------------------------------------

        source_files = repository.get(
            "source_files",
            [],
        )

        norm_sources = [s.replace("\\", "/") for s in source_files]
        if relevant_files:
            matched = []
            for rf in relevant_files:
                norm_rf = rf.replace("\\", "/")
                if norm_rf in norm_sources or rf in source_files:
                    matched.append(rf)
            # If not in disk source listing, still analyze the relevant_files directly
            files_to_analyze = (matched or relevant_files)[:3]
        else:
            files_to_analyze = source_files[:3]

        # --------------------------------------------------
        # 4. AST analysis
        # --------------------------------------------------

        ast_analysis = {}

        for relative_file in files_to_analyze:

            file_path = (
                f"{repository_path}/{relative_file}"
            )

            try:
                ast_analysis[relative_file] = (
                    self.ast_analyzer.analyze_file(
                        file_path
                    )
                )

            except (FileNotFoundError, ValueError) as exc:
                ast_analysis[relative_file] = {
                    "file": relative_file,
                    "error": str(exc),
                }

        # --------------------------------------------------
        # 5. Return unified analysis
        # --------------------------------------------------

        return {
            "repository": repository,
            "dependencies": dependencies,
            "ast_analysis": ast_analysis,
        }