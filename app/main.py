"""시연용 예제 API.

일부러 단순하게 만든 앱이다. 영상에서는 이 앱에 보안 검사(gitleaks, Trivy)를
하나씩 붙여 가며 "문제 발견 -> 수정 -> 통과" 흐름을 보여준다.
"""
import os

import requests
from fastapi import FastAPI

app = FastAPI(title="FOSS-2026-2 Demo API")

# 외부 API 키는 코드에 쓰지 않고 환경변수로 받는다.
# (시연 1에서 일부러 이 줄 대신 하드코딩한 가짜 키를 넣어 gitleaks에 걸리게 한다)
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")


@app.get("/")
def hello():
    return {"message": "안녕하세요, FOSS 2026-2 보안 게이트 예제입니다."}


@app.get("/status")
def status():
    """외부 서비스 상태를 확인하는 척하는 엔드포인트 (requests 라이브러리 사용)."""
    try:
        r = requests.get("https://www.githubstatus.com/api/v2/status.json", timeout=5)
        return {"github": r.json().get("status", {}).get("description", "unknown")}
    except requests.RequestException:
        return {"github": "unreachable"}
