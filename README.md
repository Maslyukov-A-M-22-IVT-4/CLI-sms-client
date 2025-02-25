# SMS Client CLI

Это CLI-программа для отправки SMS через API. Программа принимает параметры командной строки,
формирует HTTP-запрос и отправляет его на указанный сервер.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ваш-username/ваш-репозиторий.git
    cd ваш-репозиторий
    ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
3. Перед запуском программы создайте файл конфигурации config.toml в корне проекта. Пример содержимого:
   ```toml
   [sms_service]
   url = "localhost"  # Адрес сервиса отправки SMS
   username = "user"  # Имя пользователя
   password = "pass"  # Пароль
   ```
   
## Запуск с мок-сервером

Для тестирования программы можно использовать мок-сервер Prism.

1. Скачайте Prism для вашей платформы:

[Windows / Linux / macOS](https://github.com/stoplightio/prism/releases)

2. Поместите мок-сервер и спецификацию sms-platform.yaml в корневую папку проекта.

3. Запустите мок-сервер:
   ```bash
   ./prism-cli-win.exe mock sms-platform.yaml
   ```

   (Замените prism-cli-win.exe на prism-cli-linux или prism-cli-macos в зависимости от вашей ОС.)


4. Запустите программу с аргументами:

   ```bash
    python -m sms_client.cli --sender 123456789 --recipient 987654321 --message "Hello, World!"
   ```
   **_Все параметры командной строки обязательны для ввода!_**


5. Если все сделано правильно, то в консоль выведется сообщение:

   ```
   Response: { "status": "success", "message_id": "123456"}
   ```
   
## Тесты

Для запуска тестов выполните команду:

   ```bash
   python -m pytest tests/
   ```