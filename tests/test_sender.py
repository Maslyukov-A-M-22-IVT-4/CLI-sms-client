import pytest
from sms_client.sender import send_sms
from sms_client.http import HTTPResponse


@pytest.mark.asyncio
async def test_send_sms_success(monkeypatch):
    """Тестирует успешную отправку SMS."""

    # Мок функции asyncio.open_connection
    async def mock_open_connection(*args, **kwargs):
        class MockReader:
            @staticmethod
            async def read(_):
                return b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"

        class MockWriter:
            @staticmethod
            def write(data):
                expected_data = (
                    b"POST /send_sms HTTP/1.1\r\n"
                    b"Host: localhost\r\n"
                    b"Authorization: Basic dXNlcjpwYXNz\r\n"
                    b"Content-Type: application/json\r\n"
                    b"Content-Length: 77\r\n"
                    b"\r\n"
                    b'{"sender": "123456789", "recipient": "987654321", "message": "Hello, World!"}'
                )
                assert data == expected_data, "Отправленные данные не соответствуют ожидаемым"

            async def drain(self):
                pass

            def close(self):
                pass

            async def wait_closed(self):
                pass

        return MockReader(), MockWriter()

    # Подменяем asyncio.open_connection на мок
    monkeypatch.setattr("asyncio.open_connection", mock_open_connection)

    config = {
        "sms_service": {
            "url": "localhost",
            "username": "user",
            "password": "pass"
        }
    }

    response = await send_sms(config, "123456789", "987654321", "Hello, World!")

    assert isinstance(response, HTTPResponse), "Ответ должен быть объектом HTTPResponse"
    assert response.body == '{"status": "success"}', "Тело ответа не соответствует ожидаемому"
