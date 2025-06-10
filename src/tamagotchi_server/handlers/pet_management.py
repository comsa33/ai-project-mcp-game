import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pathlib import Path
import random

from ..models.pet import Pet, PetSpecies, PetMood, GrowthStage
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


class PetManager:
    """펫 생명체 관리 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.pets_file = self.data_dir / "pets.json"
        self.pets: Dict[str, Pet] = self._load_pets()
        
    def _load_pets(self) -> Dict[str, Pet]:
        """저장된 펫 데이터 로드"""
        if not self.pets_file.exists():
            return {}
        
        try:
            with open(self.pets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                pets = {}
                for pet_id, pet_data in data.items():
                    pets[pet_id] = Pet(**pet_data)
                return pets
        except Exception as e:
            logger.error(f"펫 데이터 로드 실패: {e}")
            return {}
    
    def _save_pets(self):
        """펫 데이터 저장"""
        try:
            data = {}
            for pet_id, pet in self.pets.items():
                data[pet_id] = pet.dict()
            
            with open(self.pets_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"펫 데이터 저장 완료: {len(self.pets)}마리")
        except Exception as e:
            logger.error(f"펫 데이터 저장 실패: {e}")
    
    def create_pet(self, name: str, species: PetSpecies, breed: Optional[str] = None) -> Pet:
        """새로운 펫 생성"""
        # 기본 성격 특성 랜덤 생성
        personality_traits = {
            "playfulness": random.randint(30, 90),
            "sociability": random.randint(20, 80),
            "curiosity": random.randint(40, 95),
            "stubbornness": random.randint(10, 70),
            "energy_level": random.randint(50, 100),
            "intelligence": random.randint(40, 90)
        }
        
        # 종족별 특성 조정
        if species == PetSpecies.DOG:
            personality_traits["sociability"] += 20
            personality_traits["playfulness"] += 15
        elif species == PetSpecies.CAT:
            personality_traits["curiosity"] += 20
            personality_traits["stubbornness"] += 15
        elif species == PetSpecies.RABBIT:
            personality_traits["curiosity"] += 10
            personality_traits["energy_level"] -= 10
        
        pet = Pet(
            name=name,
            species=species,
            breed=breed or species.value,
            personality=personality_traits
        )
        
        # 기본 특성 태그 추가
        pet.pet_nature = self._generate_nature_tags(pet)
        
        self.pets[pet.pet_id] = pet
        self._save_pets()
        
        logger.info(f"새로운 펫 생성: {pet.name} ({pet.species.value})")
        pet.add_memory("birth", f"{pet.name}이(가) 태어났습니다!", 10)
        
        return pet
    
    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """펫 조회"""
        return self.pets.get(pet_id)
    
    def get_all_pets(self) -> List[Pet]:
        """모든 펫 조회"""
        return list(self.pets.values())
    
    def update_pet_status(self, pet_id: str) -> Optional[Pet]:
        """펫 상태 자동 업데이트 (시간 경과에 따른)"""
        pet = self.get_pet(pet_id)
        if not pet or not pet.is_alive:
            return pet
        
        now = datetime.now()
        time_diff = now - pet.last_updated_at
        hours_passed = time_diff.total_seconds() / 3600
        
        if hours_passed < 0.1:  # 6분 미만이면 업데이트 안함
            return pet
        
        # 시간 경과에 따른 상태 변화
        decay_rate = max(1, int(hours_passed))
        
        # 배고픔 증가
        pet.stats.hunger = max(0, pet.stats.hunger - decay_rate * 2)
        
        # 에너지 감소 (잠들어 있으면 회복)
        if pet.is_awake:
            pet.stats.energy = max(0, pet.stats.energy - decay_rate)
        else:
            pet.stats.energy = min(100, pet.stats.energy + decay_rate * 2)
        
        # 청결도 감소
        pet.stats.cleanliness = max(0, pet.stats.cleanliness - decay_rate)
        
        # 건강도 변화 (다른 상태가 나쁘면 건강도 감소)
        if pet.stats.hunger < 20 or pet.stats.cleanliness < 20:
            pet.stats.health = max(0, pet.stats.health - decay_rate)
        elif pet.stats.hunger > 80 and pet.stats.cleanliness > 80:
            pet.stats.health = min(100, pet.stats.health + 1)
        
        # 행복도 변화
        happiness_change = 0
        if pet.stats.hunger < 30:
            happiness_change -= 2
        if pet.stats.health < 50:
            happiness_change -= 2
        if pet.stats.cleanliness < 30:
            happiness_change -= 1
        if pet.stats.energy < 20:
            happiness_change -= 1
        
        pet.stats.happiness = max(0, min(100, pet.stats.happiness + happiness_change))
        
        # 나이 증가 (하루 = 24시간)
        if hours_passed >= 24:
            days_to_add = int(hours_passed // 24)
            pet.age += days_to_add
            pet.days_alive += days_to_add
            pet.update_growth_stage()
        
        # 기분 업데이트
        pet.current_mood = self._determine_mood(pet)
        
        # 생명 상태 확인
        if pet.stats.health <= 0 or pet.stats.hunger <= 0:
            pet.current_hp = max(0, pet.current_hp - 10)
            if pet.current_hp <= 0:
                pet.is_alive = False
                pet.add_memory("death", f"{pet.name}이(가) 세상을 떠났습니다...", -50)
                logger.warning(f"펫 사망: {pet.name}")
        
        # 수면 상태 자동 조정
        if pet.stats.energy < 20 and pet.is_awake:
            pet.is_awake = False
            pet.last_sleep_at = now
            pet.add_memory("sleep", f"{pet.name}이(가) 잠들었습니다.", 0)
        elif pet.stats.energy > 80 and not pet.is_awake:
            pet.is_awake = True
            pet.add_memory("wake_up", f"{pet.name}이(가) 깨어났습니다!", 5)
        
        pet.last_updated_at = now
        self._save_pets()
        
        return pet
    
    def _generate_nature_tags(self, pet: Pet) -> List[str]:
        """성격 기반 특성 태그 생성"""
        tags = []
        
        if pet.personality.playfulness > 70:
            tags.append("활발함")
        elif pet.personality.playfulness < 30:
            tags.append("조용함")
        
        if pet.personality.sociability > 70:
            tags.append("사교적")
        elif pet.personality.sociability < 30:
            tags.append("수줍음")
        
        if pet.personality.curiosity > 70:
            tags.append("호기심")
        
        if pet.personality.stubbornness > 70:
            tags.append("고집스러움")
        elif pet.personality.stubbornness < 30:
            tags.append("순종적")
        
        if pet.personality.energy_level > 80:
            tags.append("에너지 넘침")
        elif pet.personality.energy_level < 40:
            tags.append("느긋함")
        
        if pet.personality.intelligence > 80:
            tags.append("똑똑함")
        
        return tags[:5]  # 최대 5개 태그
    
    def _determine_mood(self, pet: Pet) -> PetMood:
        """현재 상태를 기반으로 기분 결정"""
        if pet.stats.health < 30:
            return PetMood.SICK
        elif pet.stats.hunger < 20:
            return PetMood.HUNGRY
        elif pet.stats.energy < 20:
            return PetMood.SLEEPY
        elif pet.stats.happiness < 30:
            return PetMood.LONELY
        elif pet.stats.happiness > 80 and pet.stats.energy > 60:
            return random.choice([PetMood.HAPPY, PetMood.EXCITED, PetMood.PLAYFUL])
        elif pet.personality.curiosity > 70 and pet.stats.energy > 40:
            return PetMood.CURIOUS
        elif pet.stats.energy > 80 and pet.personality.playfulness > 60:
            return PetMood.PLAYFUL
        else:
            return PetMood.CALM
    
    def get_pet_status_summary(self, pet_id: str) -> Optional[Dict]:
        """펫 상태 요약 정보"""
        pet = self.get_pet(pet_id)
        if not pet:
            return None
        
        # 상태 업데이트
        pet = self.update_pet_status(pet_id)
        
        return {
            "pet_id": pet.pet_id,
            "name": pet.name,
            "species": pet.species.value,
            "age": pet.age,
            "growth_stage": pet.growth_stage.value,
            "is_alive": pet.is_alive,
            "is_awake": pet.is_awake,
            "current_mood": pet.current_mood.value,
            "overall_condition": pet.get_overall_condition(),
            "stats": {
                "hunger": pet.stats.hunger,
                "happiness": pet.stats.happiness,
                "health": pet.stats.health,
                "energy": pet.stats.energy,
                "cleanliness": pet.stats.cleanliness,
                "affection": pet.stats.affection
            },
            "needs": {
                "is_hungry": pet.is_hungry(),
                "is_unhappy": pet.is_unhappy(),
                "needs_sleep": pet.needs_sleep(),
                "is_dirty": pet.is_dirty(),
                "is_sick": pet.is_sick()
            },
            "personality_traits": pet.pet_nature,
            "favorite_activities": pet.favorite_activities,
            "recent_memories": pet.memories[-5:] if pet.memories else []
        }
    
    def delete_pet(self, pet_id: str) -> bool:
        """펫 삭제"""
        if pet_id in self.pets:
            pet_name = self.pets[pet_id].name
            del self.pets[pet_id]
            self._save_pets()
            logger.info(f"펫 삭제: {pet_name}")
            return True
        return False
    
    def get_pet_personality(self, pet_id: str) -> Optional[Dict]:
        """펫 성격 정보 조회"""
        pet = self.get_pet(pet_id)
        if not pet:
            return None
        
        return {
            "pet_id": pet.pet_id,
            "name": pet.name,
            "personality": pet.personality.dict(),
            "nature_tags": pet.pet_nature,
            "current_mood": pet.current_mood.value,
            "favorite_activities": pet.favorite_activities,
            "learned_preferences": pet.learned_preferences
        }


# 싱글톤 인스턴스
_pet_manager = None

def get_pet_manager() -> PetManager:
    """PetManager 싱글톤 인스턴스 반환"""
    global _pet_manager
    if _pet_manager is None:
        _pet_manager = PetManager()
    return _pet_manager
