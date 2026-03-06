LinkedIn Uploader — MVP 스펙

목표
- 사용자가 LinkedIn에 이미지를(프로필/게시물) 업로드할 수 있는 간단한 업로드 흐름 제공
- 백엔드에서 LinkedIn OAuth 인증 처리 및 업로드 위임
- 보안, 관찰성, 확장성 고려한 기본 구현

주요 사용자 흐름
1. 프론트엔드에서 "LinkedIn 연결" 버튼 클릭
2. OAuth2 인증 (authorization code flow) → 백엔드에서 코드 수신
3. 백엔드가 액세스 토큰을 획득하고 안전하게 저장(암호화된 비밀 저장소)
4. 사용자는 업로드 UI에서 파일 선택 → 파일은 백엔드로 전송
5. 백엔드가 LinkedIn API로 파일 업로드 → 게시물 생성 또는 프로필 사진 업데이트
6. 성공/실패 상태를 프론트엔드에 반환

핵심 요구사항 (Acceptance Criteria)
- OAuth 연결 흐름이 안전하게 동작한다 (state 검사, PKCE 권장)
- 업로드된 파일은 서버 측에서 유효성 검사(타입: image/jpeg, image/png; 최대 10MB)
- 전송 실패 시 재시도 로직(3회, 지수 백오프) 포함
- 모든 외부 요청은 타임아웃(5s) 설정
- 성공 시 응답에 LinkedIn 리소스 ID 포함

API 설계 (백엔드)
- GET /api/links/linkedin/auth-url
  - 설명: 프론트가 OAuth2 인증 URL을 가져오기 위함
  - 응답: { url: string }

- POST /api/links/linkedin/callback
  - 설명: OAuth callback 엔드포인트 (authorization code 수신)
  - 바디: { code: string, state: string }
  - 동작: 토큰 교환, 토큰 암호화 저장

- POST /api/links/linkedin/upload
  - 설명: 파일 업로드 요청
  - 인증: 사용자 세션 또는 JWT 필요
  - 바디: multipart/form-data file
  - 응답: { success: bool, linkedin_id?: string, error?: string }

보안 및 비밀관리
- 액세스 토큰/리프레시 토큰은 KMS로 암호화한 뒤 저장(예: AWS KMS + Dynamo/Postgres)
- 최소 권한 OAuth 스코프 요청
- CSRF 보호 (state 검증), PKCE 사용 권장
- 업로드 파일 바이너리 스캐닝(추후): 바이러스 검사 연동 고려

관찰성/로깅
- 주요 트랜잭션에 correlation_id 포함
- 업로드 성공/실패 카운터 및 latency(예: p95, p99)
- Prometheus metrics: linkedin_upload_requests_total, linkedin_upload_errors_total, linkedin_upload_duration_seconds
- 추적: OpenTelemetry 속성 채택 권장

운영/제약
- 레이트 리미트: LinkedIn API 한도 준수; 클라이언트 수준 60req/min 기본
- 재시도: 429/5xx에 대해 지수 백오프(최대 3회)
- 헬스체크: /health 포함(업스트림 인증 토큰 유효성 검사 옵션)

데이터 모델(간략)
- linkedin_accounts
  - id, user_id, encrypted_token, refresh_token_enc, scope, expires_at, created_at, updated_at

테스트 및 QA 기준
- OAuth 흐름 시뮬레이션 테스트 (mock LinkedIn)
- 업로드 파일 유효성 검사 유닛 테스트
- 통합 테스트: 업로드 성공/실패 케이스

개발 고려사항 및 오픈 이슈
- 프론트엔드에서 OAuth 리디렉션 URI 구성 필요 — Kevin(#ai-frontend)과 조율
- 토큰 저장소: Postgres vs Dynamo 검토 필요 (기본: Postgres)
- 보안 검토: Isabella(#ai-security) 리뷰 필요

MVP 범위 제외
- 자동 게시물 템플릿 편집 UI
- 대용량 미디어 변환 또는 CDN 변환 파이프라인

참고
- LinkedIn API 문서: https://learn.microsoft.com/en-us/linkedin/

