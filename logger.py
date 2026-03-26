import inspect
import logging
from pathlib import Path
from typing import Literal

LogLevel = int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logger(
    name: str = None,
    level: LogLevel = "INFO",
    log_file: str | None = None,
    log_to_console: bool = False,
    fmt: str = """%(asctime)s - %(levelname)s - logger:%(name)s - module:%(module)s -
    func:%(funcName)s:%(lineno)d - %(message)s""",
) -> logging.Logger:
    """
    Настраивает универсальный логгер для проекта.
    :param name: Имя логгера (обычно __name__)
    :param level: уровень логирования (по умолчанию INFO)
    :param log_file: путь к лог-файлу (если нужно логировать в файл)
    :param log_to_console: по умолчанию не создается (если нужно логировать в консоль)
    :param fmt: формат сообщения,
    :return: настроенный логгер
    """

    if name is None or log_file is None:
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame.frame)
        module_name = caller_module.__name__ if caller_module else "None"
        if name is None:
            name = module_name
        if log_file is None:
            log_file = f"{module_name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_file:
        logs_dir = Path(__file__).resolve().parent.parent / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_path = logs_dir / log_file

        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
