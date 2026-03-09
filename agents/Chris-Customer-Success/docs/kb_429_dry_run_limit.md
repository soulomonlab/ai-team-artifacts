# KB: 429 / DRY_RUN_LIMIT

요약
- 증상: API 호출 시 간헐적으로 429 응답(Too Many Requests) 또는 DRY_RUN_LIMIT 관련 에러가 발생함.
- 영향: 요청이 즉시 실패하여 사용자가 기능을 이용하지 못하거나 작업이 중단됨.

권장 응답 UX
- 프론트엔드: 비차단(non-blocking) 토스트 노출을 권장. 즉시 재시도 버튼 대신 '자동 재시도 중' 안내와 함께 사용자에게 상황을 알림.
- 접근성: 토스트는 스크린리더에 읽히도록 aria-live="polite" 사용.

사용자 메시지(카피 스니펫)
- 기본(간단): "요청량 초과로 일시적으로 이용이 지연되고 있습니다. 잠시 후 다시 시도해주세요."
- 개발자용(디버그): "429 Too Many Requests — 요청 제한에 도달했습니다. 자동 재시도를 시도합니다. (에러 코드: DRY_RUN_LIMIT)"

SDK/프론트엔드 권장 처리 (예시)
- 원칙: 지수 백오프(exponential backoff) + jitter, 최대 재시도 횟수 제한, 요청 취소(사용자가 떠날 경우).

JavaScript 예시
- pseudo-code:
  - 최대 재시도 5회
  - 초기 대기 500ms, multiplier 2, jitter 0.5

Python 예시
- requests + tenacity 사용 권장

(참고: 실제 코드 스니펫은 엔지니어가 제공한 SDK 형식에 맞춰 조정 필요)

근본 원인(가능성)
- 갑작스러운 트래픽 증가 또는 반복적인 자동화 요청
- 백엔드의 보호 룰(DRY_RUN quota) 초과

임시 해결책(Workaround)
- 클라이언트 측에서 재시도 로직 적용
- 요청 빈도(동시성) 낮추기

영구적 해결(권장)
- 백엔드: 쿼터 정책 완화 또는 보다 세밀한 rate-limiting(예: 페어링 기준)
- 프론트엔드: 사용자에게 재시도 진행 상태를 명확히 표시

문제 해결 체크리스트 (Support용)
- [ ] 정확한 에러 코드(429, DRY_RUN_LIMIT) 및 타임스탬프 수집
- [ ] 요청 헤더(사용자 ID, API 키, 엔드포인트) 수집
- [ ] 재현 단계(가능 시) 기록
- [ ] 서버 로그(관련 인스턴스, 로그 레벨) 요청
- [ ] 고객에겐 비차단 토스트 공지 및 ETA 안내

발행 메타데이터
- 작성자: Customer Success (초안)
- 파일: output/docs/kb_429_dry_run_limit.md
- 공개 URL (발행 후 업데이트): <여기에 KB URL 붙여넣기>

게시 시 요구사항 (Acceptance Criteria)
- Support KB가 퍼블릭으로 접근 가능해야 함
- KB 내 Troubleshooting 체크리스트가 포함되어야 함
- SDK/샘플 처리 권장사항이 기술되어 있어야 함
- 프론트엔드 구현 팀에게 사용할 수 있는 카피 스니펫(3개) 제공

프론트엔드 참고사항
- 토스트 컴포넌트: non-blocking, aria-live="polite"
- 데이터 속성: data-kb-url (발행된 KB URL 삽입)
- 상태 배너 우선순위: 낮음 — 사용자 흐름을 막지 않음

지원 요청 / 다음 단계
1. Emma (#ai-docs) — 이 KB를 공식 CMS에 게시하고 공개 URL을 회신해주세요. 게시 후 URL을 이 문서와 프론트엔드 팀에 전달해야 합니다.
2. Frontend — 토스트에 data-kb-url 속성으로 해당 URL을 연결해주세요.
