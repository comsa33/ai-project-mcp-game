# src/tamagotchi_server/https_server.py
"""
HTTPS 지원 HTTP MCP 서버
"""

import ssl
import uvicorn
from pathlib import Path

# 기존 http_server.py에서 app import
from .http_server import app

def create_ssl_context():
    """SSL 컨텍스트 생성 (자체 서명 인증서)"""
    # 개발용 자체 서명 인증서 생성 스크립트
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"
    
    # 자체 서명 인증서가 없으면 생성 안내
    if not cert_file.exists() or not key_file.exists():
        print("SSL 인증서가 필요합니다. 다음 명령어로 생성하세요:")
        print(f"openssl req -x509 -newkey rsa:4096 -keyout {key_file} -out {cert_file} -days 365 -nodes")
        print("Common Name에는 'ruoserver.iptime.org'를 입력하세요.")
        return None
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert_file, key_file)
    return ssl_context

if __name__ == "__main__":
    ssl_context = create_ssl_context()
    
    if ssl_context:
        # HTTPS 서버 실행
        uvicorn.run(
            "https_server:app",
            host="0.0.0.0",
            port=27777,
            ssl_keyfile="certs/key.pem",
            ssl_certfile="certs/cert.pem",
            reload=False,
            log_level="info"
        )
    else:
        # HTTP 서버 실행 (fallback)
        uvicorn.run(
            "https_server:app",
            host="0.0.0.0",
            port=27777,
            reload=False,
            log_level="info"
        )