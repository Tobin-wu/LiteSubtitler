# coding: utf8
import logging
import logging.handlers
from pathlib import Path

from config import DEFAULT_ARGS


def setup_logger(name: str,
                 level: int = DEFAULT_ARGS['LOG_SETTING'].get('level'),
                 default_fmt: str = DEFAULT_ARGS['LOG_SETTING'].get('format'),
                 date_fmt: str = '%Y-%m-%d %H:%M:%S',
                 log_file: str = str(Path(DEFAULT_ARGS['LOG_SETTING'].get('path')) / 'app.log'),
                 ) -> logging.Logger:
    """创建并配置一个日志记录器。

    根据传入的参数配置日志记录器，支持文件日志和控制台日志输出。日志文件支持轮转，避免单个文件过大。

    Args:
        name (str): 日志记录器的名称。
        level (int): 日志级别，默认为配置中的级别。
        default_fmt (str): 日志格式字符串，默认为配置中的格式。
        date_fmt (str): 时间格式字符串，默认为'%Y-%m-%d %H:%M:%S'。
        log_file (str): 日志文件路径，默认为配置中的路径下的app.log'。

    Returns:
        logging.Logger: 配置好的日志记录器对象。
    """
    logger = logging.getLogger(name)  # 获取或创建日志记录器
    logger.setLevel(level)

    # 避免重复添加处理器
    if not logger.handlers:
        formatter = logging.Formatter(default_fmt, datefmt=date_fmt)

        # 配置文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)  # 确保日志目录存在
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            print("警告：未配置日志文件路径，日志将不会写入文件。")

        # 配置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 设置特定库的日志级别为ERROR，减少日志噪音
    error_loggers = ["urllib3", "requests", "openai", "httpx", "httpcore", "ssl", "certifi"]
    for lib in error_loggers:
        logging.getLogger(lib).setLevel(logging.ERROR)

    return logger
