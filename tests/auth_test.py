def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_successful_register(client, auth):
    """Successful register redirects to the login"""
    response = auth.register()
    assert response.headers["Location"] == "/login"


def test_successful_login(client, auth):
    """Successful login redirects to the dashboard"""
    response2 = auth.register()
    response = auth.login()
    assert response.headers["Location"] == "/dashboard"

def test_dashboard_logged_in(client, auth):
    """If user is logged in can access dashboard page"""
    response1 = auth.register()
    response3 = auth.login()
    response2 = client.get("/dashboard")
    assert b"Welcome: test@email.com" in response2.data
    assert b"Dashboard" in response2.data

def test_dashboard_not_logged_in(client):
    """if user is not logged in can not access dashboard gets sent back to login page"""
    response = client.get("/dashboard")
    assert response.headers["Location"] == "/login?next=%2Fdashboard"

def test_denying_upload(client):
    """if user is not logged in can not access bank page"""
    response = client.post("/bank/upload")
    assert response.headers["Location"] == "/login?next=%2Fbank%2Fupload"

def test_bad_password_confirmation_register(client):
    response = client.post("/register", data={"email": "tester@email.com", "password": "Tester4@", "confirm": "tester"})
    print(response.data)
    assert b"Passwords must match" in response.data

def test_email_registration(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/register", data={"email": "sample", "password": "Tester1@", "confirm": "Tester1@"})
    print(response.data)
    assert b"Invalid email address." in response.data

def test_email_login(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/login", data={"email": "sample", "password": "Tester1@"})
    assert b"Invalid email address." in response.data

def test_bad_password_registration(client):
    """If password does not meets requirements"""
    response = client.post("/register", data={"email": "sample@email.com", "password": "Tester1", "confirm": "Tester1"})
    print(response.data)
    assert b"Invalid Password" in response.data

def test_bad_password_login(client):
    """If password does not meets requirements"""
    response = client.post("/login", data={"email": "sample@email.com", "password": "Tester1"})
    print(response.data)
    assert b"Invalid Password" in response.data
    