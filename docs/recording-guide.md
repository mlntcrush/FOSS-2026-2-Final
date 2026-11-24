# 녹화 가이드 (A안, 1편 약 20분)

> 이 문서는 녹화용 대본·명령 모음이다. 2026-11-24 기준 로컬에서 실제로 돌려 확인한 것은 ✅로 표시했다.

## 녹화 전 체크

- [ ] 화면 해상도 1920×1080, 터미널 글꼴 18pt 이상
- [ ] 이어폰 마이크, 스피커 끄기 (시스템 사운드는 녹음)
- [ ] OBS 등 녹화 프로그램 워터마크 없음
- [ ] GitHub에 `FOSS-2026-2-Final`, `tag-demo-action` 두 저장소가 공개(public)로 올라가 있음
- [ ] `.github/workflows/security.yml`이 0단계(hello) 상태
- [ ] `requirements.txt`의 `requests==2.19.1` 그대로
- [ ] `tag-demo-action`에 `v1` 태그 push 완료 (아래 시연 3 준비 참고)
- [ ] 리허설 1회: CI가 몇 초 걸리는지 측정 → 기다리는 동안 말할 내용 준비 (무음 구간 = 감점)

---

## 시연 1: gitleaks (약 5분)

1. **가짜 키 만들기** (진짜 키 절대 금지). 터미널에서 무작위 40자를 만든다:
   ```
   python -c "import secrets,string;print(''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(40)))"
   ```
   `app/main.py`의 `WEATHER_API_KEY = os.environ.get(...)` 줄을 아래처럼 바꾼다:
   ```python
   weather_api_key = "<방금 만든 40자>"
   ```
   - AWS 형식(`AKIA...`) 같은 실제 서비스 형식은 쓰지 않는다. GitHub 푸시 보호가 push를 막을 수 있다 [추정]. 무작위 40자는 푸시 보호에 막히지 않고 올라가며, CI의 gitleaks `generic-api-key` 룰에 잡힌다 ✅ (2026-11-24 리허설)
2. **로컬 검사**: `gitleaks dir . --redact -v` → 파일·줄·룰 이름 짚기 ✅
3. `stages/01-gitleaks.yml` 내용을 `.github/workflows/security.yml`에 붙여 넣기 → commit, push → **❌**
4. 키를 환경변수 방식으로 되돌리고 commit, push → **그래도 ❌** ✅
   - 말할 내용: "파일에서 지웠는데 왜 실패할까요? 워크플로가 커밋 기록 전체를 검사하기 때문입니다. 한 번 push된 키는 이미 유출된 것으로 봐야 합니다."
5. 해결 순서 (실무 원칙):
   1. **키 폐기(revoke)**: 실제 서비스였다면 발급처에서 키를 폐기하고 새 키를 GitHub Secrets에 등록한다 (Settings → Secrets and variables → Actions)
   2. 폐기한 키의 탐지 결과를 예외로 등록: CI 로그의 `Fingerprint:` 값을 복사해 저장소 루트에 `.gitleaksignore` 파일을 만들고 한 줄로 붙여 넣는다
   3. commit, push → **✅** ✅
   - ⚠️ `.gitleaksignore`는 **VS Code로 만들 것**. PowerShell `Set-Content`는 파일 앞에 BOM을 붙여 예외가 무시된다 (로컬에서 실제로 겪음)

## 시연 2: Trivy (약 5분)

1. `requirements.txt`의 `requests==2.19.1`을 보여준다
2. **로컬 검사**: `trivy fs --scanners vuln --severity HIGH,CRITICAL .`
   → `CVE-2018-18074 (HIGH)`, 고쳐진 버전 `2.20.0` ✅
   - 말할 내용: HTTPS에서 HTTP로 리다이렉트될 때 Authorization 헤더가 지워지지 않는 문제 → 인증 정보가 평문 구간으로 샐 수 있음
3. `stages/02-trivy.yml` 내용으로 교체 → push → **❌**
   - `exit-code: "1"` 줄을 짚기: "이 줄이 없으면 취약점이 있어도 초록불입니다"
4. `requests`를 최신 버전(2026-11-24 기준 `2.34.2`, HIGH 이상 0건 ✅)으로 올리고 push → **✅** ✅
5. Actions 실행 결과 페이지에서 `sbom` artifact를 내려받아 열어 보기 → "내 프로그램의 부품 명세서"
   - 로컬에서 보여주려면: `trivy fs --format cyclonedx --output sbom.cdx.json .`

## 시연 3: 태그 바꿔치기 재현 (약 4분), 하이라이트

### 준비 (녹화 전)
- `v1` 태그는 이미 push 완료 (2026-11-24). **원래 커밋 SHA = `0febd20e66e0121230eda75bc7bb3bea0bd33ba0`**
- 태그로 호출하면 `✅ 정상 코드입니다` 출력 확인 ✅ (리허설)
- 리허설 등으로 태그를 이미 옮겼다면 원상복구: `git tag -f v1 0febd20 && git push -f origin v1`
본 저장소에 `stages/demo-tag.yml`을 `.github/workflows/tag-demo.yml`로 복사해 push

### 녹화
1. 슬라이드: 2026-03-19 trivy-action 사건 (GHSA-69fq-xp46-6x23 / CVE-2026-33634)
   - 공격자가 탈취한 자격증명으로 태그 77개 중 76개를 악성 커밋으로 강제 이동
   - 태그로 호출하던 저장소들의 CI에서 비밀값을 훔치는 코드가 실행됨
   - 안전했던 경우: immutable release로 보호된 0.35.0 태그, 안전한 커밋에 SHA 고정
2. Actions 탭 → tag-demo → Run workflow → 출력: `✅ 정상 코드입니다`
3. `tag-demo-action`에서 `action.yml`의 echo 문구를 `⚠️ 바뀐 코드입니다 — 호출하는 쪽은 아무것도 안 바꿨습니다`로 수정:
   ```
   git commit -am "change behavior"
   git tag -f v1
   git push -f origin v1
   ```
4. 본 저장소는 **한 줄도 안 고치고** 다시 Run workflow → 출력이 `⚠️ 바뀐 코드` → "이게 공격자가 한 일입니다"
5. `tag-demo.yml`에서 `@v1`을 `@<원래 SHA> # v1`로 바꾸고 push → Run → 다시 `✅ 정상 코드`
   - 태그를 또 옮겨도 결과가 안 바뀌는 것까지 보여주면 완벽
6. `stages/03-pinned.yml`(최종본)로 교체: 모든 Action SHA 고정 + `permissions: contents: read` + `persist-credentials: false`

## 정리 (약 2분)

- 최종 `security.yml` 전체 화면
- "비밀키는 gitleaks, 부품은 Trivy, 그 둘을 자동으로 돌리는 건 Actions, 그리고 Actions 자체는 SHA 고정"
- 덤: gitleaks-action은 v2부터 MIT가 아니라서 본체를 체크섬 검증해 직접 받았다는 점 → "도구를 고를 때 라이선스도 확인하자"

## 녹화 후 정리

- 시연 3 이후 `tag-demo.yml`은 지워도 되고 남겨도 된다 (수동 실행 전용이라 평소엔 안 돈다)
- 동영상 파일은 저장소에 넣지 않는다 (`.gitignore`에 `*.mp4` 등록됨)
