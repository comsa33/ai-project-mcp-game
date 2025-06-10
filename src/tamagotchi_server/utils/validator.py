# src/tamagotchi_server/utils/validator.py
from typing import Any, Dict, List, Union, Optional
from pydantic import ValidationError
import re


class PetValidator:
    """펫 관련 데이터 검증 클래스"""
    
    @staticmethod
    def validate_pet_name(name: str) -> tuple[bool, str]:
        """펫 이름 검증"""
        if not name or not isinstance(name, str):
            return False, "이름은 필수입니다."
        
        name = name.strip()
        
        if len(name) < 1:
            return False, "이름은 최소 1글자 이상이어야 합니다."
        
        if len(name) > 20:
            return False, "이름은 최대 20글자까지 가능합니다."
        
        # 특수문자 제한 (한글, 영문, 숫자, 공백만 허용)
        if not re.match(r'^[가-힣a-zA-Z0-9\s]+$', name):
            return False, "이름에는 한글, 영문, 숫자, 공백만 사용할 수 있습니다."
        
        return True, ""
    
    @staticmethod
    def validate_species(species: str) -> tuple[bool, str]:
        """펫 종류 검증"""
        valid_species = ["개", "고양이", "토끼", "햄스터", "새"]
        
        if species not in valid_species:
            return False, f"지원하지 않는 종류입니다. 가능한 종류: {', '.join(valid_species)}"
        
        return True, ""
    
    @staticmethod
    def validate_stat_value(value: Any, stat_name: str) -> tuple[bool, str]:
        """상태 수치 검증 (0-100)"""
        try:
            value = int(value)
        except (ValueError, TypeError):
            return False, f"{stat_name}는 숫자여야 합니다."
        
        if not 0 <= value <= 100:
            return False, f"{stat_name}는 0과 100 사이의 값이어야 합니다."
        
        return True, ""
    
    @staticmethod
    def validate_personality_traits(traits: Dict[str, int]) -> tuple[bool, str]:
        """성격 특성 검증"""
        required_traits = [
            "playfulness", "sociability", "curiosity", 
            "stubbornness", "energy_level", "intelligence"
        ]
        
        for trait in required_traits:
            if trait not in traits:
                return False, f"필수 성격 특성 '{trait}'가 누락되었습니다."
            
            valid, error = PetValidator.validate_stat_value(traits[trait], trait)
            if not valid:
                return False, error
        
        return True, ""
    
    @staticmethod
    def validate_interaction_type(interaction_type: str) -> tuple[bool, str]:
        """상호작용 타입 검증"""
        valid_types = [
            "대화", "놀이", "먹이", "청소", "치료", "칭찬", "꾸중",
            "쓰다듬기", "안아주기", "산책", "수면", "깨우기"
        ]
        
        if interaction_type not in valid_types:
            return False, f"지원하지 않는 상호작용 타입입니다. 가능한 타입: {', '.join(valid_types)}"
        
        return True, ""
    
    @staticmethod
    def validate_mood_impact(impact: Any) -> tuple[bool, str]:
        """기분 영향도 검증"""
        try:
            impact = int(impact)
        except (ValueError, TypeError):
            return False, "기분 영향도는 숫자여야 합니다."
        
        if not -10 <= impact <= 10:
            return False, "기분 영향도는 -10과 10 사이의 값이어야 합니다."
        
        return True, ""
    
    @staticmethod
    def validate_pet_data(pet_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """펫 데이터 전체 검증"""
        errors = []
        
        # 이름 검증
        if "name" in pet_data:
            valid, error = PetValidator.validate_pet_name(pet_data["name"])
            if not valid:
                errors.append(error)
        
        # 종류 검증
        if "species" in pet_data:
            valid, error = PetValidator.validate_species(pet_data["species"])
            if not valid:
                errors.append(error)
        
        # 상태 수치 검증
        if "stats" in pet_data:
            stats = pet_data["stats"]
            for stat_name in ["hunger", "happiness", "health", "energy", "cleanliness", "affection"]:
                if stat_name in stats:
                    valid, error = PetValidator.validate_stat_value(stats[stat_name], stat_name)
                    if not valid:
                        errors.append(error)
        
        # 성격 검증
        if "personality" in pet_data:
            valid, error = PetValidator.validate_personality_traits(pet_data["personality"])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors


class InputSanitizer:
    """입력 데이터 정화 클래스"""
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 100) -> str:
        """문자열 정화"""
        if not isinstance(text, str):
            return ""
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        # 길이 제한
        if len(text) > max_length:
            text = text[:max_length]
        
        # 연속된 공백을 하나로 축약
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @staticmethod
    def sanitize_pet_name(name: str) -> str:
        """펫 이름 정화"""
        name = InputSanitizer.sanitize_string(name, 20)
        
        # 특수문자 제거 (한글, 영문, 숫자, 공백만 유지)
        name = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', name)
        
        return name.strip()
    
    @staticmethod
    def sanitize_description(description: str) -> str:
        """설명 텍스트 정화"""
        description = InputSanitizer.sanitize_string(description, 500)
        
        # 기본적인 HTML 태그 제거
        description = re.sub(r'<[^>]+>', '', description)
        
        return description
