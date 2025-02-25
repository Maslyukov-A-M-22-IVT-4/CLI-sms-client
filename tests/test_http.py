from sms_client.http import HTTPRequest, HTTPResponse


def test_http_request_to_bytes():
    """Тестирует метод to_bytes() класса HTTPRequest."""
    request = HTTPRequest(
        method="POST",
        url="/send_sms",
        headers={"Content-Type": "application/json", "Authorization": "Basic dXNlcjpwYXNz"},
        body='{"key": "value"}'
    )
    expected = (
        b"POST /send_sms HTTP/1.1\r\n"
        b"Content-Type: application/json\r\n"
        b"Authorization: Basic dXNlcjpwYXNz\r\n"
        b"\r\n"
        b'{"key": "value"}'
    )
    assert request.to_bytes() == expected


def test_http_request_from_bytes():
    """Тестирует метод from_bytes() класса HTTPRequest."""
    binary_data = (
        b"POST /send_sms HTTP/1.1\r\n"
        b"Content-Type: application/json\r\n"
        b"Authorization: Basic dXNlcjpwYXNz\r\n"
        b"\r\n"
        b'{"key": "value"}'
    )
    request = HTTPRequest.from_bytes(binary_data)
    assert request.method == "POST"
    assert request.url == "/send_sms"
    assert request.headers == {"Content-Type": "application/json", "Authorization": "Basic dXNlcjpwYXNz"}
    assert request.body == '{"key": "value"}'


def test_http_response_to_bytes():
    """Тестирует метод to_bytes() класса HTTPResponse."""
    response = HTTPResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body='{"status": "success"}'
    )
    expected = (
        b"HTTP/1.1 200\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )
    assert response.to_bytes() == expected


def test_http_response_from_bytes():
    """Тестирует метод from_bytes() класса HTTPResponse."""
    binary_data = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )
    response = HTTPResponse.from_bytes(binary_data)
    assert response.status_code == 200
    assert response.headers == {"Content-Type": "application/json"}
    assert response.body == '{"status": "success"}'
