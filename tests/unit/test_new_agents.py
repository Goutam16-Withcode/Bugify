from agents.security.agent import SecurityAuditAgent
from agents.performance.agent import PerformanceProfilerAgent
from agents.test_generator.agent import TestGeneratorAgent


def test_security_audit_agent_detects_unsafe_eval():
    agent = SecurityAuditAgent()
    unsafe_patch = """--- a/calc.py
+++ b/calc.py
@@ -10,1 +10,1 @@
-return safe_calc(expr)
+return eval(expr)
"""
    result = agent.audit("Expression calculator defect", unsafe_patch)
    assert result["passed"] is False
    assert result["risk_level"] in ("HIGH", "CRITICAL")
    assert any("CWE-95" in v or "eval" in v for v in result["vulnerabilities"])


def test_security_audit_agent_approves_safe_patch():
    agent = SecurityAuditAgent()
    safe_patch = """--- a/user_service.py
+++ b/user_service.py
@@ -40,2 +40,5 @@
-profile = user_repo.find_by_id(user_id).get_data()
+user = user_repo.find_by_id(user_id)
+if user is None:
+    return None
+profile = user.get_data()
"""
    result = agent.audit("AttributeError NoneType", safe_patch)
    assert result["passed"] is True
    assert result["safety_score"] >= 80


def test_performance_profiler_agent_detects_nested_loops():
    agent = PerformanceProfilerAgent()
    slow_patch = """--- a/search.py
+++ b/search.py
@@ -15,2 +15,6 @@
-return [x for x in items]
+matches = []
+for item in items:
+    for target in target_list:
+        if item == target:
+            matches.append(item)
+return matches
"""
    result = agent.profile("Search inefficiency", slow_patch)
    assert result["time_complexity_after"] in ("O(N^2)", "O(N*M)")
    assert result["impact_rating"] in ("POTENTIAL_OVERHEAD", "REGRESSION")
    assert len(result["bottlenecks"]) > 0


def test_test_generator_agent_synthesizes_pytest_suite():
    agent = TestGeneratorAgent()
    patch = """--- a/auth.py
+++ b/auth.py
@@ -5,1 +5,3 @@
-token = headers["auth"]
+token = headers.get("auth", "")
"""
    result = agent.generate_tests("KeyError auth", "KeyError: 'auth'", patch, "Missing dict key")
    assert "test_code" in result
    assert "def test_" in result["test_code"]
    assert result["test_count"] >= 1
