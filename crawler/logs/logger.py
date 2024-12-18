import logging


class Logger:

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.hasHandlers():
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            formatter = logging.Formatter("%(asctime)s [%(name)s] - %(levelname)s : %(message)s")
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger

    def log_info(self, msg: str) -> None:
        self.logger.info(msg)

    def log_warning(self, msg) -> None:
        self.logger.warning(msg)

    def log_error(self, msg) -> None:
        self.logger.error(msg)
