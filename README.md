# YouTube Metrics CLI

CLI-утилита на Python для анализа YouTube-метрик из CSV. Подробности — в [SPEC.md](SPEC.md).

Демонстрация работы CLI:

![Демонстрация работы CLI](assets/screen-cli-demo.png)

Демонстрация работы CLI pytest:

![Демонстрация работы CLI pytest](assets/screen-cli-test-demo.png)


## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Запуск

```bash
python main.py --files fixtures/valid.csv --report clickbait
```

После установки пакета:

```bash
python -m youtube_cli --files fixtures/valid.csv --report clickbait
```
