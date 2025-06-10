from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class GrowthStage(str, Enum):
    EGG = "알"
    BABY = "새끼"
    CHILD = "아이"
    TEEN = "청소년기"
    ADULT = "성인"
    ELDER = "노년기"


class PetSpecies(str, Enum):
    DOG = "개"
    CAT = "고양이"
    RABBIT = "토끼"
    HAMSTER = "햄스터"
    BIRD = "새"


class PetMood(str, Enum):
    HAPPY = "행복함"
    EXCITED = "신남"
    CURIOUS = "호기심많음"
    SLEEPY = "졸림"
    HUNGRY = "배고픔"
    LONELY = "외로움"
    PLAYFUL = "장난기"
    CALM = "차분함"
    SICK = "아픔"
    ANGRY = "화남"


class PetPersonality(BaseModel):
    """펫의 성격 특성"""
    playfulness: int = Field(default=50, ge=0, le=100, description="장난기")
    sociability: int = Field(default=50, ge=0, le=100, description="사교성")
    curiosity: int = Field(default=50, ge=0, le=100, description="호기심")
    stubbornness: int = Field(default=50, ge=0, le=100, description="고집스러움")
    energy_level: int = Field(default=50, ge=0, le=100, description="에너지 레벨")
    intelligence: int = Field(default=50, ge=0, le=100, description="지능")


class PetStats(BaseModel):
    """펫의 현재 상태 수치"""
    hunger: int = Field(default=100, ge=0, le=100, description="배고픔 (100이 가장 배부름)")
    happiness: int = Field(default=100, ge=0, le=100, description="행복도")
    health: int = Field(default=100, ge=0, le=100, description="건강도")
    energy: int = Field(default=100, ge=0, le=100, description="에너지")
    cleanliness: int = Field(default=100, ge=0, le=100, description="청결도")
    affection: int = Field(default=50, ge=0, le=100, description="애정도")


class Pet(BaseModel):
    """펫 메인 모델"""
    pet_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=20)
    species: PetSpecies
    breed: Optional[str] = None
    
    # 기본 정보
    age: int = Field(default=0, ge=0, description="나이 (일 단위)")
    weight: float = Field(default=1.0, gt=0, description="무게 (kg)")
    growth_stage: GrowthStage = Field(default=GrowthStage.EGG)
    
    # 생명 상태
    max_hp: int = Field(default=100, ge=1, le=200)
    current_hp: int = Field(default=100, ge=0, le=200)
    is_alive: bool = Field(default=True)
    is_awake: bool = Field(default=True)
    
    # 상태 수치
    stats: PetStats = Field(default_factory=PetStats)
    
    # 성격
    personality: PetPersonality = Field(default_factory=PetPersonality)
    
    # AI 관련 데이터
    current_mood: PetMood = Field(default=PetMood.HAPPY)
    pet_nature: List[str] = Field(default_factory=list, description="펫의 특성 태그들")
    favorite_activities: List[str] = Field(default_factory=list)
    learned_preferences: dict = Field(default_factory=dict)
    memories: List[dict] = Field(default_factory=list)
    
    # 시간 관련
    created_at: datetime = Field(default_factory=datetime.now)
    last_fed_at: Optional[datetime] = None
    last_played_at: Optional[datetime] = None
    last_cleaned_at: Optional[datetime] = None
    last_sleep_at: Optional[datetime] = None
    last_updated_at: datetime = Field(default_factory=datetime.now)
    
    # 통계
    total_meals: int = Field(default=0)
    total_play_sessions: int = Field(default=0)
    total_baths: int = Field(default=0)
    days_alive: int = Field(default=0)

    def is_hungry(self) -> bool:
        """배고픈 상태인지 확인"""
        return self.stats.hunger < 30

    def is_unhappy(self) -> bool:
        """불행한 상태인지 확인"""
        return self.stats.happiness < 30

    def needs_sleep(self) -> bool:
        """잠이 필요한지 확인"""
        return self.stats.energy < 20

    def is_dirty(self) -> bool:
        """더러운 상태인지 확인"""
        return self.stats.cleanliness < 30

    def is_sick(self) -> bool:
        """아픈 상태인지 확인"""
        return self.stats.health < 50 or self.current_hp < self.max_hp * 0.5

    def get_overall_condition(self) -> str:
        """전체적인 컨디션 평가"""
        avg_stats = (
            self.stats.hunger + 
            self.stats.happiness + 
            self.stats.health + 
            self.stats.energy + 
            self.stats.cleanliness
        ) / 5
        
        if avg_stats >= 80:
            return "최상"
        elif avg_stats >= 60:
            return "좋음"
        elif avg_stats >= 40:
            return "보통"
        elif avg_stats >= 20:
            return "나쁨"
        else:
            return "위험"

    def update_growth_stage(self):
        """나이에 따른 성장 단계 업데이트"""
        if self.age < 1:
            self.growth_stage = GrowthStage.EGG
        elif self.age < 7:
            self.growth_stage = GrowthStage.BABY
        elif self.age < 30:
            self.growth_stage = GrowthStage.CHILD
        elif self.age < 90:
            self.growth_stage = GrowthStage.TEEN
        elif self.age < 200:
            self.growth_stage = GrowthStage.ADULT
        else:
            self.growth_stage = GrowthStage.ELDER

    def add_memory(self, event_type: str, description: str, mood_impact: int = 0):
        """새로운 기억 추가"""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "description": description,
            "mood_impact": mood_impact,
            "age_at_event": self.age
        }
        self.memories.append(memory)
        
        # 최근 100개 기억만 유지
        if len(self.memories) > 100:
            self.memories = self.memories[-100:]

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }