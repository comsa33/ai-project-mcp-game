# src/tamagotchi_server/utils/config.py
import os
from typing import Dict, Any
from pathlib import Path


class Config:
    """설정 관리 클래스"""
    
    def __init__(self):
        self.data_dir = os.getenv("TAMAGOTCHI_DATA_DIR", "data")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.max_pets_per_user = int(os.getenv("MAX_PETS_PER_USER", "5"))
        self.auto_save_interval = int(os.getenv("AUTO_SAVE_INTERVAL", "300"))  # 5분
        
        # 게임 밸런스 설정
        self.hunger_decay_rate = float(os.getenv("HUNGER_DECAY_RATE", "2.0"))
        self.energy_decay_rate = float(os.getenv("ENERGY_DECAY_RATE", "1.0"))
        self.cleanliness_decay_rate = float(os.getenv("CLEANLINESS_DECAY_RATE", "1.0"))
        self.health_decay_rate = float(os.getenv("HEALTH_DECAY_RATE", "0.5"))
        
        # 펫 수명 관련
        self.max_pet_age_days = int(os.getenv("MAX_PET_AGE_DAYS", "200"))
        self.critical_health_threshold = int(os.getenv("CRITICAL_HEALTH_THRESHOLD", "20"))
        
        # 디렉토리 생성
        Path(self.data_dir).mkdir(exist_ok=True)
    
    def get_growth_stages(self) -> Dict[str, int]:
        """성장 단계별 필요 일수"""
        return {
            "알": 0,
            "새끼": 1,
            "아이": 7,
            "청소년기": 30,
            "성인": 90,
            "노년기": 200
        }
    
    def get_species_traits(self) -> Dict[str, Dict[str, int]]:
        """종족별 기본 특성"""
        return {
            "개": {
                "sociability_bonus": 20,
                "playfulness_bonus": 15,
                "base_weight": 3.0
            },
            "고양이": {
                "curiosity_bonus": 20,
                "stubbornness_bonus": 15,
                "base_weight": 2.0
            },
            "토끼": {
                "curiosity_bonus": 10,
                "energy_penalty": 10,
                "base_weight": 1.5
            },
            "햄스터": {
                "energy_bonus": 15,
                "sociability_penalty": 10,
                "base_weight": 0.3
            },
            "새": {
                "intelligence_bonus": 15,
                "curiosity_bonus": 10,
                "base_weight": 0.5
            }
        }


_config = None

def get_config() -> Config:
    """Config 싱글톤 인스턴스 반환"""
    global _config
    if _config is None:
        _config = Config()
    return _config
