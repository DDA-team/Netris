# Netris

Бэкэнд и фронтэнд собираются отдельно. 

Для запуска бэка необходимо установить: fastapi, uvicorn, SQLAlchemy, python-multipart, aiofiles, opencv.
Для работы нейросетевого решения необходимо установить: torch, ultralytics

Зависимости фронта указаны в packages.json
Запуск и сборку проекта лучше всего производить через vue-cli командой vue-cli-service build. Также можно воспользоваться vue ui

Запуск бэка производится через uvicorn или аналогичный ASGI-server. Документация доступна через route /docs

Запуск нейросетевого воркера(worker.py) производится через стандартный интепретатор python
