from typing import Dict, Self


class HTTPRequest:
    def __init__(self, method: str, url: str, headers: Dict[str, str], body: str = ""):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """
        Преобразует HTTP-запрос в байтовую строку.
        """
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        request_str = f"{self.method} {self.url} HTTP/1.1\r\n{headers_str}\r\n\r\n{self.body}"
        return request_str.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        """
        Создает объект HTTP-запроса из байтовой строки.

        :param binary_data: Байтовое представление HTTP-запроса.
        :return: Объект HTTP-запроса.
        """
        data = binary_data.decode("utf-8")
        lines = data.split("\r\n")

        # Парсим первую строку (метод, URL, протокол)
        if not lines:
            raise ValueError("Empty HTTP request")
        request_line = lines[0].split()
        if len(request_line) != 3:
            raise ValueError("Invalid HTTP request line")
        method, url, _ = request_line

        # Парсим заголовки
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            if ": " not in lines[i]:
                raise ValueError(f"Invalid header format: {lines[i]}")
            key, value = lines[i].split(": ", 1)
            headers[key] = value
            i += 1

        # Парсим тело запроса
        body = lines[i + 1] if i + 1 < len(lines) else ""

        return cls(method, url, headers, body)


class HTTPResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        """
        Преобразует HTTP-ответ в байтовую строку.
        """
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        response_str = f"HTTP/1.1 {self.status_code}\r\n{headers_str}\r\n\r\n{self.body}"
        return response_str.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        """
        Создает объект HTTP-ответа из байтовой строки.

        :param binary_data: Байтовое представление HTTP-ответа.
        :return: Объект HTTP-ответа.
        """
        data = binary_data.decode("utf-8")
        try:
            headers, body = data.split("\r\n\r\n", 1)
        except ValueError:
            raise ValueError("Invalid HTTP response format")

        lines = headers.split("\r\n")
        if not lines:
            raise ValueError("Empty HTTP response")

        # Парсим статус-код
        status_line = lines[0]
        parts = status_line.split(" ")
        if len(parts) < 2:
            raise ValueError("Invalid status line")
        try:
            status_code = int(parts[1])
        except ValueError:
            raise ValueError("Invalid status code")

        # Парсим заголовки
        headers_dict = {}
        for line in lines[1:]:
            if ": " not in line:
                continue
            key, value = line.split(": ", 1)
            headers_dict[key] = value

        return cls(status_code, headers_dict, body)
