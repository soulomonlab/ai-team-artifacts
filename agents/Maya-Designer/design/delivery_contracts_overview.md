상황 (Situation)
- 목표: WebSocket + Webhook 기반의 Delivery Contracts (메시지 전달 계약)을 정의하여 실시간 전달과 서버-to-server 이벤트 콜백을 안정적으로 지원.

복잡성 (Complication)
- 기술적 세부사항(메시지 스키마, 인증, 재시도 로직 등)은 백엔드에서 결정되어야 하지만, 사용자(경험) 관점의 흐름과 실패/재연결 UX 요구사항이 명확히 정의되어 있어야 설계가 사용자 친화적이다.

해결 (Resolution) — 결론 우선
- output/design/delivery_contracts_overview.md 생성. 이 문서는 UX 중심의 메시지 흐름, 구독 모델, 인증/상태표시 UX, 재시도/백오프/데드레터 처리의 사용자 관점 요구사항과 예시 페이로드를 포함. 백엔드(정밀 스펙)는 Marcus에게 전달하여 output/specs/delivery_contracts_api_spec.md 작성 요청.

① 핵심 요청 재진술 (The real ask)
- WebSocket과 Webhook 둘 다를 위한 전달 계약을 정의: 메시지 JSON 스키마(예시), 구독 모델(주제/채널/필터), 인증(토큰/서명), 하트비트 및 재연결 규칙, Webhook 페이로드/서명/재시도/백오프/DLQ 포맷, 레이트 리미트. 최종 산출물: 기술 API 스펙 + 예시 페이로드.

② MECE 분해 (Mutually Exclusive, Collectively Exhaustive)
A. WebSocket
  A1. 메시지 스키마 (event 타입, metadata, payload)
  A2. 구독 모델 (channels, topics, filters, wildcard)
  A3. 인증/권한 (initial handshake token, per-subscription auth)
  A4. 연결 유지 (heartbeat/ping-pong), idle timeout
  A5. 재연결 전략 (exponential backoff, resume vs fresh reconnect)
  A6. 클라이언트 UX 상태 (connected / connecting / disconnected / retrying)

B. Webhook
  B1. 페이로드 스키마 (event envelope, metadata, payload)
  B2. 서명/검증 (HMAC, key rotation guidance)
  B3. 전송 보장 (at-least-once semantics, idempotency keys)
  B4. 재시도/백오프 정책 (retry count, backoff strategy, DLQ format)
  B5. 레이트 리밋 및 보호 (per-target, global)

C. 운영·보안·개발자 경험
  C1. 모니터링/관찰성 (delivery metrics, success/failure rates)
  C2. 관용성(Dead Letter Queue format, visibility)
  C3. 개발자 문서/예제 (curl, SDK 예시, sample payloads)

③ 소유자(Assign each sub-question)
- Marcus (Backend): 전 범위의 기술적 API 스펙(스키마, 인증, 서명, 재시도, DLQ 포맷, 레이트 리밋)을 작성. (핵심 담당자)
- Kevin (Frontend): WebSocket 상태/구독 UX 및 재연결 UI 컴포넌트 구현. (보조 담당자)
- Maya (Designer, 본인): UX 관점 문서화 + 메시지/에러 흐름, 예시 페이로드(샘플) 제공 — 현 파일을 생성.
- Dana (QA): 테스팅 시나리오(재연결, 중복 수신, DLQ 확인) 작성. (handoff 이후 요청 예정)

④ Maya(Designer) 작업 시작 — 내가 할 것 (this workstream)
- UX 중심 문서(output/design/delivery_contracts_overview.md):
  - 사용자 관점의 연결/구독/에러 흐름 정의
  - 상태 표시 및 권장 UI 동작(예: 연결 끊김 시 재시도 UX, 실시간 표시)
  - Webhook 관리 화면에서 필요한 정보(엔드포인트 등록, 서명 키, 리트라이 설정, DLQ 보기)
  - 예시 페이로드(간단한 JSON) — 참고용
  - Acceptance criteria for backend spec (what I need Marcus to deliver)

문서 주요 내용 (요약)
1) WebSocket — UX 흐름
   - 연결 단계: connecting -> connected -> subscribed
   - 구독: client sends SUBSCRIBE {topic, filter} → server returns SUBSCRIBED {subscription_id}
   - 연결 끊김 UX: 자동 재연결(지수 백오프), 사용자에게 toast + persistent status bar에 '연결 끊김 — 재시도 중 (n초)' 표시
   - Resume vs Fresh reconnect: 가능하면 resume을 지원(서버가 last-seen offset을 유지). 불가 시 re-sync 가이드(요청 시 과거 N초 이벤트 재전송).
   - Heartbeat: 서버 ping, 클라이언트 pong; heartbeat miss = 2 intervals → 상태 변경 및 재연결 시도.

2) Webhook — UX/관리 화면 요구사항
   - 엔드포인트 등록 폼: URL, description, headers (optional), signing secret (auto-generate / rotate)
   - Delivery settings: max retries, backoff strategy (linear/exponential), DLQ enable toggle
   - Test delivery button + sample payload preview
   - Delivery history table: timestamp, status (200/4xx/5xx), attempts, response snippet, link to DLQ item

3) Error handling & observability (UX)
   - 사용자에게 중요한 것: 실패/성공 비율, 평균 지연, 최근 실패 원인 요약
   - DLQ 뷰: failed_event_id, original_payload (masked PII), error_reason, retry button (manual), requeue button

4) Sample payloads (간단 예제 — 기술 스펙 작성 시 확장 필요)
- WebSocket event (notification):
  {
    "event_type": "order.created",
    "event_id": "evt_01F...",
    "timestamp": "2026-03-09T12:34:56Z",
    "payload": { "order_id": "ord_123", "amount": 1200, "currency": "USD" }
  }

- Webhook envelope:
  {
    "event_type": "order.created",
    "event_id": "evt_01F...",
    "timestamp": "2026-03-09T12:34:56Z",
    "delivery_id": "del_abc",
    "attempt": 1,
    "payload": { "order_id": "ord_123", "amount": 1200 }
  }

- Webhook signing header example (HMAC-SHA256):
  X-Signature: sha256=hex(HMAC(secret, body))

5) Acceptance criteria for backend spec (what I expect Marcus to deliver)
   - Formal JSON Schema for WebSocket events + envelope
   - Subscription API: SUBSCRIBE/UNSUBSCRIBE message formats and server responses
   - Authentication: handshake token format, expiry, refresh, per-subscription auth rules
   - Heartbeat: interval, timeout thresholds, server/client behaviors
   - Reconnection: resume semantics, offset/token for resume, backoff parameters
   - Webhook: exact envelope fields, signing algorithm + rotation strategy, retry/backoff algorithm (params), DLQ format/schema, idempotency guidance, rate limits (per-target and global)
   - Example cURL and SDK snippets for both WS and Webhook
   - Security considerations (replay protection, signature rotation, PII handling)

결정 기록 (Decisions made / Recommendations)
- UX recommendation: 연결 상태는 앱 상단의 persistent status component로 노출.
- 권장 서명: HMAC-SHA256 with key rotation. 이유: 널리 사용되며 검증 비용이 낮음.
- 재시도 권장: exponential backoff with jitter, max attempts = 5 (configurable). 이유: balance between delivery guarantee and not overwhelming targets.

파일 생성 위치
- output/design/delivery_contracts_overview.md (이 파일)

다음 단계
- Marcus에게 기술적 스펙 작성을 요청합니다: output/specs/delivery_contracts_api_spec.md 생성 (정밀 JSON Schema, auth, signing, retry, DLQ 포맷 포함).

