# GitHub Actions 보안 게이트 입문: gitleaks·Trivy로 비밀키 유출과 공급망 공격 막기

FOSS 2026-2 기말 프로젝트 (소프트웨어 툴타임) · 정준영

- 영상: (업로드 후 링크 추가)
- 라이선스: MIT

## 1. 주제를 고른 이유

<!-- 작성: 왜 이 도구를 친구들에게 알려 주고 싶었는지 (3~4줄) -->

## 2. 기존 영상과의 관계

<!-- 작성: 2024년 "AWS CodePipeline + SCA DevSecOps" 시리즈를 직접 보고, 무엇을 보완·대체하는지 구체적으로.
     예: AWS 계정 없이 무료 GitHub Actions만으로 구성 / 비밀키 검사·SBOM 추가 /
         2026년 3월 trivy-action 공급망 공격 이후의 대응(커밋 SHA 고정) 반영 -->

## 3. 사용한 도구

| 도구 | 역할 | 라이선스 |
|---|---|---|
| GitHub Actions | push·PR마다 검사를 자동 실행 | 공개 저장소 무료 |
| gitleaks v8.30.1 | 코드와 커밋 기록 전체에서 비밀키 탐지 | MIT |
| Trivy v0.76.2 (trivy-action v0.36.0) | 의존성 취약점(CVE) 검사, SBOM 생성 | Apache-2.0 |

## 4. 저장소 구성

```
app/main.py                    시연용 예제 API (FastAPI)
requirements.txt               일부러 취약한 버전(requests 2.19.1) 포함
.github/workflows/security.yml 보안 검사 워크플로 (녹화 시작 시 0단계)
stages/01-gitleaks.yml         1단계: gitleaks
stages/02-trivy.yml            2단계: + Trivy, SBOM
stages/03-pinned.yml           3단계(최종): 커밋 SHA 고정 + 최소 권한
stages/demo-tag.yml            태그 바꿔치기 재현용 (tag-demo-action 저장소와 함께 사용)
docs/recording-guide.md        시연 절차와 명령
docs/script.md                 영상 대본·가이드라인·설명
slides/                        강의 PPTX
```

## 5. 사용법

1. 이 저장소를 fork 또는 clone
2. `stages/` 파일을 순서대로 `.github/workflows/security.yml`에 붙여 넣고 push
3. Actions 탭에서 결과(✅/❌) 확인
4. 로컬에서 먼저 돌려 보려면:
   ```
   gitleaks dir . --redact -v
   trivy fs --scanners vuln --severity HIGH,CRITICAL .
   ```

## 6. 배운 점·느낀 점

<!-- 작성: 직접 해 보며 놀란 점, 예상과 달랐던 점 (예: 키를 지워도 CI가 계속 실패한 이유, 보안 도구 자체가 공격받은 사건) -->

## 참고 자료

- Aqua Security, Trivy 공급망 사고 권고: https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23
- gitleaks: https://github.com/gitleaks/gitleaks
- Trivy: https://github.com/aquasecurity/trivy
