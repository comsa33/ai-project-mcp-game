# src/tamagotchi_server/mcp_tools.py
"""
MCP 서버 도구들 - Claude AI가 호출할 수 있는 펫 관리 함수들
"""

from typing import Optional, Dict, Any
from .models.pet import PetSpecies
from .handlers.pet_management import get_pet_manager
from .utils.logger import get_logger

logger = get_logger(__name__)

# PetManager 인스턴스
pet_manager = get_pet_manager()


async def create_pet(name: str, species: str, breed: Optional[str] = None) -> Dict[str, Any]:
    """
    새로운 펫을 생성합니다.
    
    Args:
        name: 펫의 이름 (1-20자)
        species: 펫의 종류 (개, 고양이, 토끼, 햄스터, 새)
        breed: 펫의 품종 (선택사항)
    
    Returns:
        생성된 펫의 정보
    """
    try:
        # 종류 검증
        species_map = {
            "개": PetSpecies.DOG,
            "고양이": PetSpecies.CAT,
            "토끼": PetSpecies.RABBIT,
            "햄스터": PetSpecies.HAMSTER,
            "새": PetSpecies.BIRD
        }
        
        if species not in species_map:
            return {
                "success": False,
                "error": f"지원하지 않는 종류입니다. 가능한 종류: {list(species_map.keys())}"
            }
        
        pet = pet_manager.create_pet(name, species_map[species], breed)
        
        return {
            "success": True,
            "pet": {
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species.value,
                "breed": pet.breed,
                "age": pet.age,
                "growth_stage": pet.growth_stage.value,
                "personality_traits": pet.pet_nature,
                "created_at": pet.created_at.isoformat()
            },
            "message": f"{pet.name}이(가) 성공적으로 태어났습니다! 🐣"
        }
    
    except Exception as e:
        logger.error(f"펫 생성 실패: {e}")
        return {
            "success": False,
            "error": f"펫 생성 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_status(pet_id: str) -> Dict[str, Any]:
    """
    펫의 현재 상태를 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 상태 정보
    """
    try:
        status = pet_manager.get_pet_status_summary(pet_id)
        
        if not status:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "status": status,
            "message": f"{status['name']}의 현재 상태입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 상태 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 상태 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def update_pet_status(pet_id: str) -> Dict[str, Any]:
    """
    시간 경과에 따른 펫의 상태를 자동 업데이트합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        업데이트된 펫의 상태 정보
    """
    try:
        pet = pet_manager.update_pet_status(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        status = pet_manager.get_pet_status_summary(pet_id)
        
        return {
            "success": True,
            "status": status,
            "message": f"{pet.name}의 상태가 업데이트되었습니다."
        }
    
    except Exception as e:
        logger.error(f"펫 상태 업데이트 실패: {e}")
        return {
            "success": False,
            "error": f"펫 상태 업데이트 중 오류가 발생했습니다: {str(e)}"
        }


async def get_all_pets() -> Dict[str, Any]:
    """
    모든 펫의 목록을 조회합니다.
    
    Returns:
        모든 펫의 기본 정보 목록
    """
    try:
        pets = pet_manager.get_all_pets()
        
        pets_info = []
        for pet in pets:
            # 각 펫의 상태 업데이트
            pet_manager.update_pet_status(pet.pet_id)
            
            pets_info.append({
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species.value,
                "age": pet.age,
                "growth_stage": pet.growth_stage.value,
                "is_alive": pet.is_alive,
                "current_mood": pet.current_mood.value,
                "overall_condition": pet.get_overall_condition()
            })
        
        return {
            "success": True,
            "pets": pets_info,
            "total_count": len(pets_info),
            "message": f"총 {len(pets_info)}마리의 펫을 찾았습니다."
        }
    
    except Exception as e:
        logger.error(f"펫 목록 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 목록 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_personality(pet_id: str) -> Dict[str, Any]:
    """
    펫의 성격과 개성 정보를 조회합니다. (AI 반응형 특화 기능)
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 성격 및 개성 데이터
    """
    try:
        personality_info = pet_manager.get_pet_personality(pet_id)
        
        if not personality_info:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "personality": personality_info,
            "message": f"{personality_info['name']}의 성격 정보입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 성격 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 성격 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_memories(pet_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    펫의 최근 기억들을 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
        limit: 조회할 기억의 개수 (기본값: 10)
    
    Returns:
        펫의 기억 목록
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        recent_memories = pet.memories[-limit:] if pet.memories else []
        
        return {
            "success": True,
            "memories": recent_memories,
            "total_memories": len(pet.memories),
            "message": f"{pet.name}의 최근 기억 {len(recent_memories)}개입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 기억 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 기억 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def check_pet_needs(pet_id: str) -> Dict[str, Any]:
    """
    펫의 현재 필요사항을 확인합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫이 필요로 하는 것들의 목록
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        # 상태 업데이트
        pet = pet_manager.update_pet_status(pet_id)
        
        needs = []
        urgency_level = "normal"
        
        if not pet.is_alive:
            return {
                "success": True,
                "needs": ["안식"],
                "urgency": "none",
                "message": f"{pet.name}이(가) 세상을 떠났습니다..."
            }
        
        if pet.is_hungry():
            needs.append("먹이")
            if pet.stats.hunger < 10:
                urgency_level = "critical"
        
        if pet.is_unhappy():
            needs.append("관심과 사랑")
            if pet.stats.happiness < 10:
                urgency_level = "critical"
        
        if pet.needs_sleep():
            needs.append("휴식")
            if pet.stats.energy < 10:
                urgency_level = "high"
        
        if pet.is_dirty():
            needs.append("목욕")
            if pet.stats.cleanliness < 10:
                urgency_level = "high"
        
        if pet.is_sick():
            needs.append("치료")
            urgency_level = "high"
        
        if not needs:
            needs.append("현재 모든 것이 만족스럽습니다")
            urgency_level = "none"
        
        return {
            "success": True,
            "needs": needs,
            "urgency": urgency_level,
            "current_mood": pet.current_mood.value,
            "message": f"{pet.name}의 현재 필요사항입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 필요사항 확인 실패: {e}")
        return {
            "success": False,
            "error": f"펫 필요사항 확인 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_growth_info(pet_id: str) -> Dict[str, Any]:
    """
    펫의 성장 관련 정보를 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 성장 단계 및 관련 정보
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        # 다음 성장 단계까지 필요한 일수 계산
        next_stage_days = 0
        next_stage = ""
        
        if pet.growth_stage.value == "알":
            next_stage_days = 1 - pet.age
            next_stage = "새끼"
        elif pet.growth_stage.value == "새끼":
            next_stage_days = 7 - pet.age
            next_stage = "아이"
        elif pet.growth_stage.value == "아이":
            next_stage_days = 30 - pet.age
            next_stage = "청소년기"
        elif pet.growth_stage.value == "청소년기":
            next_stage_days = 90 - pet.age
            next_stage = "성인"
        elif pet.growth_stage.value == "성인":
            next_stage_days = 200 - pet.age
            next_stage = "노년기"
        else:
            next_stage = "최종 단계"
        
        return {
            "success": True,
            "growth_info": {
                "current_stage": pet.growth_stage.value,
                "age_days": pet.age,
                "days_alive": pet.days_alive,
                "weight": pet.weight,
                "next_stage": next_stage,
                "days_to_next_stage": max(0, next_stage_days),
                "life_stage_progress": min(100, (pet.age / 200) * 100)  # 200일을 최대 수명으로 가정
            },
            "message": f"{pet.name}은(는) 현재 {pet.growth_stage.value} 단계입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 성장 정보 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 성장 정보 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def record_interaction(pet_id: str, interaction_type: str, description: str, mood_impact: int = 0) -> Dict[str, Any]:
    """
    사용자와 펫의 상호작용을 기록합니다. (AI 반응형 특화 기능)
    
    Args:
        pet_id: 펫의 고유 ID
        interaction_type: 상호작용 유형 (예: "대화", "놀이", "먹이", "청소")
        description: 상호작용 설명
        mood_impact: 기분에 미치는 영향 (-10 ~ +10)
    
    Returns:
        상호작용 기록 결과
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        if not pet.is_alive:
            return {
                "success": False,
                "error": f"{pet.name}이(가) 이미 세상을 떠났습니다."
            }
        
        # 기억 추가
        pet.add_memory(interaction_type, description, mood_impact)
        
        # 기분 영향 적용
        if mood_impact != 0:
            pet.stats.happiness = max(0, min(100, pet.stats.happiness + mood_impact))
            pet.stats.affection = max(0, min(100, pet.stats.affection + abs(mood_impact) // 2))
        
        # 상호작용 유형별 추가 효과
        if interaction_type == "대화":
            pet.stats.happiness = min(100, pet.stats.happiness + 2)
        elif interaction_type == "칭찬":
            pet.stats.happiness = min(100, pet.stats.happiness + 5)
            pet.stats.affection = min(100, pet.stats.affection + 3)
        
        pet_manager._save_pets()
        
        return {
            "success": True,
            "interaction": {
                "type": interaction_type,
                "description": description,
                "mood_impact": mood_impact,
                "pet_response": f"{pet.name}이(가) {interaction_type}에 반응하고 있습니다."
            },
            "current_mood": pet.current_mood.value,
            "happiness": pet.stats.happiness,
            "affection": pet.stats.affection,
            "message": f"{pet.name}과의 상호작용이 기록되었습니다."
        }
    
    except Exception as e:
        logger.error(f"상호작용 기록 실패: {e}")
        return {
            "success": False,
            "error": f"상호작용 기록 중 오류가 발생했습니다: {str(e)}"
        }


async def delete_pet(pet_id: str) -> Dict[str, Any]:
    """
    펫을 삭제합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        삭제 결과
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        pet_name = pet.name
        success = pet_manager.delete_pet(pet_id)
        
        if success:
            return {
                "success": True,
                "message": f"{pet_name}이(가) 삭제되었습니다."
            }
        else:
            return {
                "success": False,
                "error": "펫 삭제에 실패했습니다."
            }
    
    except Exception as e:
        logger.error(f"펫 삭제 실패: {e}")
        return {
            "success": False,
            "error": f"펫 삭제 중 오류가 발생했습니다: {str(e)}"
        }
    """
    새로운 펫을 생성합니다.
    
    Args:
        name: 펫의 이름 (1-20자)
        species: 펫의 종류 (개, 고양이, 토끼, 햄스터, 새)
        breed: 펫의 품종 (선택사항)
    
    Returns:
        생성된 펫의 정보
    """
    try:
        # 종류 검증
        species_map = {
            "개": PetSpecies.DOG,
            "고양이": PetSpecies.CAT,
            "토끼": PetSpecies.RABBIT,
            "햄스터": PetSpecies.HAMSTER,
            "새": PetSpecies.BIRD
        }
        
        if species not in species_map:
            return {
                "success": False,
                "error": f"지원하지 않는 종류입니다. 가능한 종류: {list(species_map.keys())}"
            }
        
        pet = pet_manager.create_pet(name, species_map[species], breed)
        
        return {
            "success": True,
            "pet": {
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species.value,
                "breed": pet.breed,
                "age": pet.age,
                "growth_stage": pet.growth_stage.value,
                "personality_traits": pet.pet_nature,
                "created_at": pet.created_at.isoformat()
            },
            "message": f"{pet.name}이(가) 성공적으로 태어났습니다! 🐣"
        }
    
    except Exception as e:
        logger.error(f"펫 생성 실패: {e}")
        return {
            "success": False,
            "error": f"펫 생성 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_status(pet_id: str) -> Dict[str, Any]:
    """
    펫의 현재 상태를 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 상태 정보
    """
    try:
        status = pet_manager.get_pet_status_summary(pet_id)
        
        if not status:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "status": status,
            "message": f"{status['name']}의 현재 상태입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 상태 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 상태 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def update_pet_status(pet_id: str) -> Dict[str, Any]:
    """
    시간 경과에 따른 펫의 상태를 자동 업데이트합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        업데이트된 펫의 상태 정보
    """
    try:
        pet = pet_manager.update_pet_status(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        status = pet_manager.get_pet_status_summary(pet_id)
        
        return {
            "success": True,
            "status": status,
            "message": f"{pet.name}의 상태가 업데이트되었습니다."
        }
    
    except Exception as e:
        logger.error(f"펫 상태 업데이트 실패: {e}")
        return {
            "success": False,
            "error": f"펫 상태 업데이트 중 오류가 발생했습니다: {str(e)}"
        }


async def get_all_pets() -> Dict[str, Any]:
    """
    모든 펫의 목록을 조회합니다.
    
    Returns:
        모든 펫의 기본 정보 목록
    """
    try:
        pets = pet_manager.get_all_pets()
        
        pets_info = []
        for pet in pets:
            # 각 펫의 상태 업데이트
            pet_manager.update_pet_status(pet.pet_id)
            
            pets_info.append({
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species.value,
                "age": pet.age,
                "growth_stage": pet.growth_stage.value,
                "is_alive": pet.is_alive,
                "current_mood": pet.current_mood.value,
                "overall_condition": pet.get_overall_condition()
            })
        
        return {
            "success": True,
            "pets": pets_info,
            "total_count": len(pets_info),
            "message": f"총 {len(pets_info)}마리의 펫을 찾았습니다."
        }
    
    except Exception as e:
        logger.error(f"펫 목록 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 목록 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_personality(pet_id: str) -> Dict[str, Any]:
    """
    펫의 성격과 개성 정보를 조회합니다. (AI 반응형 특화 기능)
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 성격 및 개성 데이터
    """
    try:
        personality_info = pet_manager.get_pet_personality(pet_id)
        
        if not personality_info:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "personality": personality_info,
            "message": f"{personality_info['name']}의 성격 정보입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 성격 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 성격 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_memories(pet_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    펫의 최근 기억들을 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
        limit: 조회할 기억의 개수 (기본값: 10)
    
    Returns:
        펫의 기억 목록
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        recent_memories = pet.memories[-limit:] if pet.memories else []
        
        return {
            "success": True,
            "memories": recent_memories,
            "total_memories": len(pet.memories),
            "message": f"{pet.name}의 최근 기억 {len(recent_memories)}개입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 기억 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 기억 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def check_pet_needs(pet_id: str) -> Dict[str, Any]:
    """
    펫의 현재 필요사항을 확인합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫이 필요로 하는 것들의 목록
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        # 상태 업데이트
        pet = pet_manager.update_pet_status(pet_id)
        
        needs = []
        urgency_level = "normal"
        
        if not pet.is_alive:
            return {
                "success": True,
                "needs": ["안식"],
                "urgency": "none",
                "message": f"{pet.name}이(가) 세상을 떠났습니다..."
            }
        
        if pet.is_hungry():
            needs.append("먹이")
            if pet.stats.hunger < 10:
                urgency_level = "critical"
        
        if pet.is_unhappy():
            needs.append("관심과 사랑")
            if pet.stats.happiness < 10:
                urgency_level = "critical"
        
        if pet.needs_sleep():
            needs.append("휴식")
            if pet.stats.energy < 10:
                urgency_level = "high"
        
        if pet.is_dirty():
            needs.append("목욕")
            if pet.stats.cleanliness < 10:
                urgency_level = "high"
        
        if pet.is_sick():
            needs.append("치료")
            urgency_level = "high"
        
        if not needs:
            needs.append("현재 모든 것이 만족스럽습니다")
            urgency_level = "none"
        
        return {
            "success": True,
            "needs": needs,
            "urgency": urgency_level,
            "current_mood": pet.current_mood.value,
            "message": f"{pet.name}의 현재 필요사항입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 필요사항 확인 실패: {e}")
        return {
            "success": False,
            "error": f"펫 필요사항 확인 중 오류가 발생했습니다: {str(e)}"
        }


async def get_pet_growth_info(pet_id: str) -> Dict[str, Any]:
    """
    펫의 성장 관련 정보를 조회합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        펫의 성장 단계 및 관련 정보
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        # 다음 성장 단계까지 필요한 일수 계산
        next_stage_days = 0
        next_stage = ""
        
        if pet.growth_stage.value == "알":
            next_stage_days = 1 - pet.age
            next_stage = "새끼"
        elif pet.growth_stage.value == "새끼":
            next_stage_days = 7 - pet.age
            next_stage = "아이"
        elif pet.growth_stage.value == "아이":
            next_stage_days = 30 - pet.age
            next_stage = "청소년기"
        elif pet.growth_stage.value == "청소년기":
            next_stage_days = 90 - pet.age
            next_stage = "성인"
        elif pet.growth_stage.value == "성인":
            next_stage_days = 200 - pet.age
            next_stage = "노년기"
        else:
            next_stage = "최종 단계"
        
        return {
            "success": True,
            "growth_info": {
                "current_stage": pet.growth_stage.value,
                "age_days": pet.age,
                "days_alive": pet.days_alive,
                "weight": pet.weight,
                "next_stage": next_stage,
                "days_to_next_stage": max(0, next_stage_days),
                "life_stage_progress": min(100, (pet.age / 200) * 100)  # 200일을 최대 수명으로 가정
            },
            "message": f"{pet.name}은(는) 현재 {pet.growth_stage.value} 단계입니다."
        }
    
    except Exception as e:
        logger.error(f"펫 성장 정보 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 성장 정보 조회 중 오류가 발생했습니다: {str(e)}"
        }


async def record_interaction(pet_id: str, interaction_type: str, description: str, mood_impact: int = 0) -> Dict[str, Any]:
    """
    사용자와 펫의 상호작용을 기록합니다. (AI 반응형 특화 기능)
    
    Args:
        pet_id: 펫의 고유 ID
        interaction_type: 상호작용 유형 (예: "대화", "놀이", "먹이", "청소")
        description: 상호작용 설명
        mood_impact: 기분에 미치는 영향 (-10 ~ +10)
    
    Returns:
        상호작용 기록 결과
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        if not pet.is_alive:
            return {
                "success": False,
                "error": f"{pet.name}이(가) 이미 세상을 떠났습니다."
            }
        
        # 기억 추가
        pet.add_memory(interaction_type, description, mood_impact)
        
        # 기분 영향 적용
        if mood_impact != 0:
            pet.stats.happiness = max(0, min(100, pet.stats.happiness + mood_impact))
            pet.stats.affection = max(0, min(100, pet.stats.affection + abs(mood_impact) // 2))
        
        # 상호작용 유형별 추가 효과
        if interaction_type == "대화":
            pet.stats.happiness = min(100, pet.stats.happiness + 2)
        elif interaction_type == "칭찬":
            pet.stats.happiness = min(100, pet.stats.happiness + 5)
            pet.stats.affection = min(100, pet.stats.affection + 3)
        
        pet_manager._save_pets()
        
        return {
            "success": True,
            "interaction": {
                "type": interaction_type,
                "description": description,
                "mood_impact": mood_impact,
                "pet_response": f"{pet.name}이(가) {interaction_type}에 반응하고 있습니다."
            },
            "current_mood": pet.current_mood.value,
            "happiness": pet.stats.happiness,
            "affection": pet.stats.affection,
            "message": f"{pet.name}과의 상호작용이 기록되었습니다."
        }
    
    except Exception as e:
        logger.error(f"상호작용 기록 실패: {e}")
        return {
            "success": False,
            "error": f"상호작용 기록 중 오류가 발생했습니다: {str(e)}"
        }


async def delete_pet(pet_id: str) -> Dict[str, Any]:
    """
    펫을 삭제합니다.
    
    Args:
        pet_id: 펫의 고유 ID
    
    Returns:
        삭제 결과
    """
    try:
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        pet_name = pet.name
        success = pet_manager.delete_pet(pet_id)
        
        if success:
            return {
                "success": True,
                "message": f"{pet_name}이(가) 삭제되었습니다."
            }
        else:
            return {
                "success": False,
                "error": "펫 삭제에 실패했습니다."
            }
    
    except Exception as e:
        logger.error(f"펫 삭제 실패: {e}")
        return {
            "success": False,
            "error": f"펫 삭제 중 오류가 발생했습니다: {str(e)}"
        }
