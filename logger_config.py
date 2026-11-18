import logging


class ColorFormatter(logging.Formatter):
    # Цветовые коды ANSI для терминала
    COLORS = {
        logging.DEBUG: "\033[36m",      # Голубой
        logging.INFO: "\033[32m",       # Зеленый
        logging.WARNING: "\033[33m",    # Желтый
        logging.ERROR: "\033[31m",      # Красный
        logging.CRITICAL: "\033[1;31m"  # Жирный красный
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        # Красим только слово уровня (например, INFO или WARNING), оставляя текст обычным
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logger() -> None:
    handler = logging.StreamHandler()
    # Формат: Время | Уровень | Сообщение
    formatter = ColorFormatter(
        fmt="%(asctime)s | %(levelname)-17s | %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)

    # Настраиваем корневой логгер, чтобы подхватились и логи самого aiogram
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)