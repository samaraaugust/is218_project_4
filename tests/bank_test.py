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
