import os
import sys
from typing import Dict, List, Optional
import google.generativeai as genai

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from src.tamagotchi_server.handlers.pet_management import get_pet_manager
from src.tamagotchi_server.utils.logger import get_logger
from src.tamagotchi_server.utils.config import get_config

logger = get_logger(__name__)
config = get_config()

# Gemini API 설정
genai.configure(api_key=config.gemini_api_key)  #gemini_api_key를 환경변수로 추가해서 적용 필요 export GEMINI_API_KEY=your_api_key 
model = genai.GenerativeModel('gemini-2.0-flash')

def get_pet_personality(pet_id: str) -> Dict[str, any]:
    """
    펫의 개성 데이터를 Gemini API를 통해 자연스러운 설명으로 변환하여 반환합니다.
    
    Args:
        pet_id (str): 펫의 고유 ID
        
    Returns:
        Dict[str, any]: 펫의 개성 정보를 담은 딕셔너리
    """
    try:
        pet_manager = get_pet_manager()
        pet = pet_manager.get_pet(pet_id)
        
        if not pet:
            return {
                "success": False,
                "error": "해당 ID의 펫을 찾을 수 없습니다."
            }
        
        # Gemini API에 전달할 프롬프트 생성
        prompt = f"""
        다음은 펫의 개성 데이터입니다. 이 데이터를 바탕으로 펫의 성격을 자연스럽게 설명해주세요.
        
        이름: {pet.name}
        품종: {pet.breed}
        나이: {pet.age}살
        무게: {pet.weight}kg
        생존 상태: {"살아있음" if pet.is_alive else "사망"}
        깨어있는 상태: {"깨어있음" if pet.is_awake else "수면중"}
        개성 특성: {', '.join(pet.pet_nature)}
        
        성격 수치:
        - 장난기: {pet.personality.playfulness}/100
        - 사교성: {pet.personality.sociability}/100
        - 호기심: {pet.personality.curiosity}/100
        - 고집스러움: {pet.personality.stubbornness}/100
        - 에너지 레벨: {pet.personality.energy_level}/100
        - 지능: {pet.personality.intelligence}/100
        
        위 데이터를 바탕으로 펫의 성격을 자연스러운 문장으로 설명해주세요.
        설명은 2-3문장 정도로 간단명료하게 작성해주세요.
        """
        
        # Gemini API 호출
        response = model.generate_content(prompt)
        description = response.text.strip()
        
        return {
            "success": True,
            "name": pet.name,
            "breed": pet.breed,
            "age": pet.age,
            "weight": pet.weight,
            "is_alive": pet.is_alive,
            "is_awake": pet.is_awake,
            "pet_nature": pet.pet_nature,
            "personality": {
                "playfulness": pet.personality.playfulness,
                "sociability": pet.personality.sociability,
                "curiosity": pet.personality.curiosity,
                "stubbornness": pet.personality.stubbornness,
                "energy_level": pet.personality.energy_level,
                "intelligence": pet.personality.intelligence
            },
            "description": description
        }
        
    except Exception as e:
        logger.error(f"펫 개성 조회 실패: {e}")
        return {
            "success": False,
            "error": f"펫 개성 조회 중 오류가 발생했습니다: {str(e)}"
        }

if __name__ == "__main__":
    # 테스트 코드 - 실제 존재하는 펫 ID 사용
    test_pet_id = "06e29629-6b12-4ac3-9355-2e907c995d35"  # 루댕이의 ID
    result = get_pet_personality(test_pet_id)
    print("\n=== 펫 개성 정보 ===")
    print(f"이름: {result.get('name', 'N/A')}")
    print(f"품종: {result.get('breed', 'N/A')}")
    print(f"개성 특성: {', '.join(result.get('pet_nature', []))}")
    print(f"\n설명:\n{result.get('description', 'N/A')}")
    print("\n전체 응답:")
    print(result)