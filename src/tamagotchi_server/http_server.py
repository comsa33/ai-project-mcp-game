# src/tamagotchi_server/http_server.py
"""
HTTP/SSE 방식 MCP 서버 - 원격 접속 지원
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from pathlib import Path
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tamagotchi_server.handlers.pet_management import get_pet_manager
from tamagotchi_server import mcp_tools
from tamagotchi_server.utils.logger import get_logger
from tamagotchi_server.utils.config import get_config

logger = get_logger(__name__)
config = get_config()

# 전역 변수
pet_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 생명주기 관리"""
    global pet_manager
    
    # 시작 시 초기화
    logger.info("=== AI 다마고치 HTTP MCP 서버 시작 ===")
    logger.info(f"데이터 디렉토리: {config.data_dir}")
    
    pet_manager = get_pet_manager()
    existing_pets = pet_manager.get_all_pets()
    logger.info(f"기존 펫 {len(existing_pets)}마리 로드됨")
    
    # 기존 펫들의 상태 업데이트
    for pet in existing_pets:
        pet_manager.update_pet_status(pet.pet_id)
    
    logger.info("HTTP MCP 서버 초기화 완료!")
    
    yield
    
    # 종료 시 정리
    logger.info("HTTP MCP 서버 종료 중...")
    if pet_manager:
        pet_manager._save_pets()
        logger.info("펫 데이터 최종 저장 완료")

# FastAPI 앱 생성
app = FastAPI(
    title="AI 다마고치 펫 게임 MCP 서버",
    description="AI 기반 다마고치 펫 관리 게임 - HTTP/SSE MCP 서버",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP 도구 매핑
MCP_TOOLS = {
    "create_pet": mcp_tools.create_pet,
    "get_pet_status": mcp_tools.get_pet_status,
    "update_pet_status": mcp_tools.update_pet_status,
    "get_all_pets": mcp_tools.get_all_pets,
    "get_pet_personality": mcp_tools.get_pet_personality,
    "get_pet_memories": mcp_tools.get_pet_memories,
    "check_pet_needs": mcp_tools.check_pet_needs,
    "get_pet_growth_info": mcp_tools.get_pet_growth_info,
    "record_interaction": mcp_tools.record_interaction,
    "delete_pet": mcp_tools.delete_pet,
}

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "AI 다마고치 펫 게임 MCP 서버",
        "version": "1.0.0",
        "team": "3조 알GO싶조",
        "mcp_endpoint": "/sse",
        "tools_count": len(MCP_TOOLS),
        "available_tools": list(MCP_TOOLS.keys())
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "pets_count": len(pet_manager.get_all_pets()) if pet_manager else 0,
        "server": "running"
    }

@app.get("/sse")
async def sse_endpoint_get(request: Request):
    """SSE GET 엔드포인트 - EventSource 연결용"""
    async def event_stream():
        # SSE 초기 연결 응답
        yield "data: {\"jsonrpc\":\"2.0\",\"method\":\"server/ready\",\"params\":{}}\n\n"
        
        # 연결 유지
        try:
            while True:
                await asyncio.sleep(1)
                # 헬스체크 이벤트
                yield f"data: {{\"jsonrpc\":\"2.0\",\"method\":\"server/heartbeat\",\"params\":{{\"timestamp\":\"{asyncio.get_event_loop().time()}\"}}}}\n\n"
        except asyncio.CancelledError:
            logger.info("SSE 연결 종료")
            return
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/sse")
async def sse_endpoint(request: Request):
    """SSE 방식 MCP 엔드포인트"""
    try:
        body = await request.json()
        
        # MCP 메시지 처리
        if body.get("jsonrpc") != "2.0":
            raise HTTPException(status_code=400, detail="Invalid JSON-RPC version")
        
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        
        logger.info(f"MCP 요청: {method} - {params}")
        
        # 메서드별 처리
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "tamagotchi-pet-game",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "notifications/initialized":
            # 초기화 완료 알림 - 응답 불필요
            logger.info("클라이언트 초기화 완료")
            return {"status": "acknowledged"}
            
        elif method == "tools/list":
            tools = []
            for tool_name, tool_func in MCP_TOOLS.items():
                # 함수의 docstring에서 도구 정보 추출
                doc = tool_func.__doc__ or ""
                description = doc.split('\n')[1].strip() if '\n' in doc else tool_name
                
                # 함수 시그니처에서 파라미터 정보 추출
                import inspect
                sig = inspect.signature(tool_func)
                
                properties = {}
                required = []
                
                for param_name, param in sig.parameters.items():
                    if param_name == 'self':
                        continue
                        
                    param_type = "string"  # 기본값
                    if param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == bool:
                        param_type = "boolean"
                    elif param.annotation == float:
                        param_type = "number"
                    
                    properties[param_name] = {
                        "type": param_type,
                        "description": f"{param_name} parameter"
                    }
                    
                    if param.default == param.empty:
                        required.append(param_name)
                
                tools.append({
                    "name": tool_name,
                    "description": description,
                    "inputSchema": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                })
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools
                }
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name not in MCP_TOOLS:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
            try:
                # 도구 실행
                tool_func = MCP_TOOLS[tool_name]
                result = await tool_func(**arguments)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                }
                
            except Exception as e:
                logger.error(f"도구 실행 오류: {e}")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"도구 실행 실패: {str(e)}"
                    }
                }
        
        else:
            # 알 수 없는 메서드에 대한 에러 응답
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {method} not supported"
                }
            }
        
        logger.info(f"MCP 응답: {response}")
        return response
        
    except Exception as e:
        logger.error(f"SSE 엔드포인트 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def list_tools():
    """사용 가능한 도구 목록"""
    tools_info = {}
    for tool_name, tool_func in MCP_TOOLS.items():
        doc = tool_func.__doc__ or ""
        description = doc.split('\n')[1].strip() if '\n' in doc else tool_name
        tools_info[tool_name] = {
            "description": description,
            "function": tool_func.__name__
        }
    
    return {
        "tools": tools_info,
        "total_count": len(tools_info)
    }

@app.post("/tools/{tool_name}")
async def call_tool_direct(tool_name: str, params: Dict[str, Any]):
    """도구 직접 호출 (테스트용)"""
    if tool_name not in MCP_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    try:
        tool_func = MCP_TOOLS[tool_name]
        result = await tool_func(**params)
        return result
    except Exception as e:
        logger.error(f"도구 실행 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 개발용 서버 실행
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=27777,
        reload=True,
        log_level="info"
    )