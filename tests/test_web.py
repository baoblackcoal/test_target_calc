from pycalc.web.app import create_app


def test_home_page_loads() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "pycalc" in body
    assert "Session History" in body


def test_web_calculates_valid_expression() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/calculate", data={"expression": "1 + 2 * 3"})

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Result:" in body
    assert "7" in body


def test_web_shows_error_for_invalid_expression() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/calculate", data={"expression": "1 / 0"})

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Error:" in body
    assert "Division by zero is not allowed." in body


def test_web_keeps_recent_history_first() -> None:
    app = create_app()
    client = app.test_client()

    client.post("/calculate", data={"expression": "1 + 1"})
    response = client.post("/calculate", data={"expression": "3 * 3"})

    body = response.get_data(as_text=True)
    latest_index = body.index("3 * 3")
    older_index = body.index("1 + 1")
    assert latest_index < older_index
