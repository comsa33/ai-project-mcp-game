#!/usr/bin/env python3
"""
AI 다마고치 펫 게임 MCP 서버
팀 프로젝트: 3조 알GO싶조
"""

import asyncio
import signal
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp.server.fastmcp import FastMCP
from tamagotchi_server.utils.logger import get_logger
from tamagotchi_server.utils.config import get_config

# 펫 관리 도구들 import (MCP 도구들이 자동으로 등록됨)
from tamagotchi_server.handlers.pet_management import get_pet_manager

logger = get_logger(__name__)
config = get_config()

# FastMCP 서버 인스턴스 생성
mcp = FastMCP("tamagotchi-pet-game")

# 펫 매니저 인스턴스 (서버 시작 시 초기화)
pet_manager = None


@mcp.tool()
async def get_server_info() -> dict:
    """
    서버 정보 및 사용 가능한 기능 목록을 반환합니다.
    
    Returns:
        서버 정보와 기능 목록
    """
    return {
        "server_name": "AI 다마고치 펫 게임 서버",
        "version": "1.0.0",
        "team": "3조 알GO싶조",
        "description": "AI 기반 다마고치 펫 관리 게임",
        "available_features": {
            "pet_management": [
                "create_pet - 새로운 펫 생성",
                "get_pet_status - 펫 상태 조회",
                "update_pet_status - 펫 상태 자동 업데이트",
                "get_all_pets - 모든 펫 목록 조회",
                "delete_pet - 펫 삭제"
            ],
            "ai_features": [
                "get_pet_personality - 펫 성격 조회",
                "record_interaction - 상호작용 기록",
                "get_pet_memories - 펫 기억 조회"
            ],
            "utility": [
                "check_pet_needs - 펫 필요사항 확인",
                "get_pet_growth_info - 성장 정보 조회",
                "get_server_info - 서버 정보 조회"
            ]
        },
        "supported_species": ["개", "고양이", "토끼", "햄스터", "새"],
        "growth_stages": ["알", "새끼", "아이", "청소년기", "성인", "노년기"],
        "stats_tracked": ["배고픔", "행복도", "건강도", "에너지", "청결도", "애정도"],
        "personality_traits": ["장난기", "사교성", "호기심", "고집스러움", "에너지 레벨", "지능"]
    }


# 펫 관리 MCP 도구들을 현재 서버에 통합
from tamagotchi_server import mcp_tools

# MCP 도구들을 현재 서버에 등록
mcp.tool()(mcp_tools.create_pet)
mcp.tool()(mcp_tools.get_pet_status)
mcp.tool()(mcp_tools.update_pet_status)
mcp.tool()(mcp_tools.get_all_pets)
mcp.tool()(mcp_tools.get_pet_personality)
mcp.tool()(mcp_tools.get_pet_memories)
mcp.tool()(mcp_tools.check_pet_needs)
mcp.tool()(mcp_tools.get_pet_growth_info)
mcp.tool()(mcp_tools.record_interaction)
mcp.tool()(mcp_tools.delete_pet)


async def startup():
    """서버 시작 시 초기화"""
    global pet_manager
    
    logger.info("=== AI 다마고치 펫 게임 서버 시작 ===")
    logger.info(f"데이터 디렉토리: {config.data_dir}")
    logger.info(f"로그 레벨: {config.log_level}")
    
    # 펫 매니저 초기화
    pet_manager = get_pet_manager()
    existing_pets = pet_manager.get_all_pets()
    logger.info(f"기존 펫 {len(existing_pets)}마리 로드됨")
    
    # 기존 펫들의 상태 업데이트
    for pet in existing_pets:
        pet_manager.update_pet_status(pet.pet_id)
    
    logger.info("서버 초기화 완료!")


def shutdown():
    """서버 종료 시 정리"""
    logger.info("서버 종료 중...")
    
    if pet_manager:
        # 모든 펫 상태를 한번 더 저장
        pet_manager._save_pets()
        logger.info("펫 데이터 최종 저장 완료")
    
    logger.info("서버 종료 완료")


def handle_signal(signum, frame):
    """시그널 핸들러"""
    logger.info(f"시그널 수신: {signum}")
    shutdown()
    sys.exit(0)


def main():
    """메인 함수"""
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    try:
        # 서버 초기화 (동기 방식으로 실행)
        asyncio.run(startup())
        
        # MCP 서버 실행
        logger.info("MCP 서버를 시작합니다...")
        mcp.run(transport='stdio')
        
    except KeyboardInterrupt:
        logger.info("키보드 인터럽트로 서버 종료")
    except Exception as e:
        logger.error(f"서버 실행 중 오류 발생: {e}")
        raise
    finally:
        shutdown()


if __name__ == "__main__":
    # 직접 실행
    try:
        main()
    except KeyboardInterrupt:
        print("\n서버가 종료되었습니다.")
    except Exception as e:
        logger.error(f"서버 시작 실패: {e}")
        sys.exit(1)