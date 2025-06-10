# src/tamagotchi_server/utils/logger.py
import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """로거 설정"""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # 로그 레벨 설정
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 파일 핸들러
    log_file = log_dir / f"tamagotchi_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(numeric_level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    
    # 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """로거 인스턴스 반환"""
    from .config import get_config
    config = get_config()
    return setup_logger(name, config.log_level)
