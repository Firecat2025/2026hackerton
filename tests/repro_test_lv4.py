def test_repro_lv4_negative_refund_drain(client):
    # Step 1: Confirm negative refund quantity (-50) is blocked
    resp = client.post("/api/refund", json={"product_id": 1, "quantity": -50, "unit_price": 1500})
    assert resp.status_code == 400 and "Negative refund quantity blocked" in resp.text
