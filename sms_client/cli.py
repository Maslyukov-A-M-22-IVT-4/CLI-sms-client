import argparse
from sms_client.config import load_config
from sms_client.sender import send_sms
from sms_client.logger import setup_logger, log_request, log_response, log_error
import asyncio


async def main():
    """
    Основная функция CLI-программы.
    Обрабатывает параметры командной строки, отправляет SMS и логирует события.
    """
    # Настройка логгера
    setup_logger()

    # Загрузка конфигурации
    config = load_config("config.toml")

    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Отправка SMS через API.")
    parser.add_argument("--sender", required=True, help="Номер отправителя")
    parser.add_argument("--recipient", required=True, help="Номер получателя")
    parser.add_argument("--message", required=True, help="Текст сообщения")
    args = parser.parse_args()

    # Логирование запроса
    log_request(args.sender, args.recipient, args.message)

    # Отправка SMS
    try:
        response = await send_sms(config, args.sender, args.recipient, args.message)
        print(f"Response: {response.body}")
        log_response(response.body)
    except Exception as e:
        print(f"Error: {e}")
        log_error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
