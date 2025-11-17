"""
Centralized rotating logger for Text-Speech Converter Pro.

Provides structured, rotating file logging with console output.
Automatically creates logs/ directory on first use.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_logger(name: str = "TextSpeechPro") -> logging.Logger:
    """
    Return a configured logger with rotating file handler and console output.
    
    Features:
    - Auto-creates logs/ directory
    - 5 MB per file, keeps 5 backup files
    - Structured format with timestamp, module, and line number
    - Prevents duplicate handlers in repeated calls
    """
    logger = logging.getLogger(name)

    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Rotating file handler (5 MB × 5 backups)
    file_handler = RotatingFileHandler(
        log_dir / "converter.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(levelname)s → %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger