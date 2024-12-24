# Request Logger

Request Logger — это простое Flask-приложение, которое позволяет логировать входящие POST-запросы и отображать их в удобном интерфейсе. Приложение поддерживает базовую авторизацию для защиты доступа к логам.

## Функциональность

- Логирование всех входящих POST-запросов, включая:
  - Дата и время запроса (с миллисекундами)
  - Метод запроса (например, POST)
  - URL, с которого был отправлен запрос
  - Заголовки запроса
  - Тело запроса
- Удобный интерфейс для просмотра логов с возможностью сворачивания/разворачивания деталей запроса.
- Базовая авторизация для защиты доступа к логам.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone <URL_вашего_репозитория>
   cd <имя_папки_репозитория>