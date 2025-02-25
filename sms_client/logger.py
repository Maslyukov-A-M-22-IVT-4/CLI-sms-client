import logging
import os

os.makedirs("logs", exist_ok=True)


def setup_logger():
    """Настраивает основной логгер."""
    logging.basicConfig(
        filename=os.path.join("logs", "sms_client.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def setup_error_logger():
    """
    Настраивает логгер для записи ошибок.
    Возвращает объект логгера.
    """
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)

    # Создаем обработчик для записи в файл errors.log
    handler = logging.FileHandler(os.path.join("logs", "errors.log"))
    handler.setLevel(logging.ERROR)

    # Устанавливаем формат сообщений
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    error_logger.addHandler(handler)

    return error_logger


def log_request(sender: str, recipient: str, message: str):
    """Логирует параметры запроса в основной лог-файл 'sms_client'."""
    logging.info(f"Отправка SMS: sender={sender}, recipient={recipient}, message={message}")


def log_response(response: str):
    """Логирует ответ сервера в основной лог-файл 'sms_client'."""
    logging.info(f"Получен ответ: {response}")


def log_error(error: str):
    """
    Логирует ошибки в отдельный файл `errors.log`.
    """
    error_logger = setup_error_logger()
    error_logger.error(error)
