import asyncio
import json
import base64
from sms_client.http import HTTPRequest, HTTPResponse
from typing import Dict, Any


async def   send_sms(config: Dict[str, Any], sender: str, recipient: str, message: str) -> HTTPResponse:
    """Асинхронно отправляет SMS через API."""
    url = config["sms_service"]["url"]
    username = config["sms_service"]["username"]
    password = config["sms_service"]["password"]
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    request_data = {
        "sender": sender,
        "recipient": recipient,
        "message": message
    }
    request_body = json.dumps(request_data)

    # Формируем HTTP-запрос
    headers = {
        "Host": url,
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
        "Content-Length": str(len(request_body))
    }
    request = HTTPRequest("POST", "/send_sms", headers, request_body)

    # Отправляем запрос через asyncio
    try:
        reader, writer = await asyncio.open_connection(url, 4010)
        writer.write(request.to_bytes())
        await writer.drain()

        response_data = await reader.read(4096)
        writer.close()
        await writer.wait_closed()

        return HTTPResponse.from_bytes(response_data)
    except Exception as e:
        raise RuntimeError(f"Error sending SMS: {e}")
