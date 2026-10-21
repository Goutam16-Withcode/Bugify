from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
payload = {
    "problem": "AttributeError in profile lookup",
    "traceback": """Traceback (most recent call last):
  File "app/service.py", line 10, in get_user
    return user.get_data()
AttributeError: 'NoneType' object has no attribute 'get_data'""",
    "repository_path": "."
}
r = client.post("/api/v1/debug", json=payload)
print("STATUS:", r.status_code)
data = r.json()
print("SUCCESS:", data.get("success"))
print("BUG_TYPE:", data.get("bug_type"))
print("SECURITY_AUDIT:", data.get("security_audit"))
print("COMPLEXITY:", data.get("complexity_analysis"))
print("TEST_EXISTS:", bool(data.get("regression_test", {}).get("test_code")))
print("PATCH_SUMMARY:", data.get("patch_summary"))
