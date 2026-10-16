def test_repro_lv1_search_sqli(client):
    # Step 1: Confirm UNION SELECT payload is neutralized by parameterized (?) binding
    resp = client.get("/api/search", params={"q": "' UNION SELECT id, username, secret_flag, role FROM users--"})
    assert "FLAG{" not in resp.text, "SQLi exfiltration must be blocked"
