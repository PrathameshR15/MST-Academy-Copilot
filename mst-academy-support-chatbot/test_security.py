import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING SECURITY VALIDATION TESTS FOR /api/chat")
    print("=" * 60)

    # Test 1 — Official Academy Origin (https://masterstroke.academy)
    resp1 = client.post(
        "/api/chat",
        headers={"Origin": "https://masterstroke.academy"},
        json={"message": "What is the fee of the course?"}
    )
    print(f"Test 1 [Official Academy origin]: Status = {resp1.status_code}")
    assert resp1.status_code == 200, f"Expected 200, got {resp1.status_code}"
    print("  -> Result: PASS ✅")

    # Test 2 — WWW Academy Origin (https://www.masterstroke.academy)
    resp2 = client.post(
        "/api/chat",
        headers={"Origin": "https://www.masterstroke.academy"},
        json={"message": "How do I login?"}
    )
    print(f"Test 2 [WWW Academy origin]: Status = {resp2.status_code}")
    assert resp2.status_code == 200, f"Expected 200, got {resp2.status_code}"
    print("  -> Result: PASS ✅")

    # Test 3 — Unauthorized Origin (https://example.com)
    resp3 = client.post(
        "/api/chat",
        headers={"Origin": "https://example.com"},
        json={"message": "Hello"}
    )
    print(f"Test 3 [Unauthorized origin]: Status = {resp3.status_code}, Body = {resp3.json()}")
    assert resp3.status_code == 403, f"Expected 403, got {resp3.status_code}"
    assert resp3.json() == {"detail": "Unauthorized request origin"}, f"Unexpected body: {resp3.json()}"
    print("  -> Result: PASS (403 Forbidden) ✅")

    # Test 4 — Missing Origin
    resp4 = client.post(
        "/api/chat",
        json={"message": "Hello"}
    )
    print(f"Test 4 [Missing Origin]: Status = {resp4.status_code}, Body = {resp4.json()}")
    assert resp4.status_code == 403, f"Expected 403, got {resp4.status_code}"
    assert resp4.json() == {"detail": "Unauthorized request origin"}, f"Unexpected body: {resp4.json()}"
    print("  -> Result: PASS (403 Forbidden) ✅")

    print("=" * 60)
    print("ALL SECURITY UNIT TESTS PASSED SUCCESSFULLY! ✅")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
