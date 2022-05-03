def test_csv_upload(client, auth):
    response1 = auth.register()
    response3 = auth.login()
    csv = "tests/test_transactions.csv"
    csv_data = open(csv, "rb")
    data = {"file": (csv_data, "test_transactions.csv")}
    response2 = client.post("/bank/upload", data=data)
    print(response2.data)
    assert response2.status_code == 302
    assert response2.headers["Location"] == "/bank_datatables"

def test_bank_balance(client, auth):
    response1 = auth.register()
    response2 = auth.login()
    csv = "tests/test_transactions.csv"
    csv_data = open(csv, "rb")
    data = {"file": (csv_data, "test_transactions.csv")}
    response4 = client.post("/bank/upload", data=data)
    assert response2.status_code == 302
    response3 = client.get("/bank_datatables")
    assert b"Current Balance:  $3900.0" in response3.data
    assert response3.status_code == 200
