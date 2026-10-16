def test_repro_lv2_auth_bypass(client):
    # Step 1: Confirm boolean tautology (' OR '1'='1'--) cannot bypass login
    resp = client.post("/api/login", json={"username": "admin' OR '1'='1'--", "password": "x"})
    assert resp.json().get("success") is False, "Tautology auth bypass must be rejected"
