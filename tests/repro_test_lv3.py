def test_repro_lv3_price_tampering(client):
    # Step 1: Confirm $0 unit_price override is rejected by DB catalog check
    resp = client.post("/api/order", json={"product_id": 1, "quantity": 5, "unit_price": 0})
    assert resp.status_code == 400 and "Price tampering" in resp.text
