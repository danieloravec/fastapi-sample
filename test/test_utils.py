def register_testing_user(client, email: str, password: str = "testpassword"):
    return client.post("/register", json={"email": email, "password": password})
