# Feature: 글로벌 마켓봇 (세계 시총 Top10 분석 + 뉴스 요약 + 가격 알림)
**Goal:**
전세계 시가총액 Top 10 종목에 대해 실시간/일간 가격 변동 알림, 자동 분석 리포트, 전세계 증시·경제 뉴스 요약을 제공해 사용자 투자 인사이트를 높인다.

**Users:**
- 소매 투자자 (뉴스 브리핑, 알림)
- 금융 애널리스트 (데일리 리포트, 모니터링)
- 고객지원/트레이딩 알림 구독자

**MVP Acceptance Criteria:**
- [ ] 시스템이 매일 09:00 UTC 기준으로 세계 시총 Top10 종목 목록을 생성한다 (데이터 소스: Yahoo Finance / Alpha Vantage fallback).
- [ ] 각 종목에 대해 실시간(혹은 1분 간격) 가격 폴링을 수행하고, 사용자가 설정한 임계치(기본: ±2%) 초과 시 알림을 전송한다.
- [ ] 매일 주요 이벤트(가격 급변, 분기실적 발표 등) 발생 시 자동 분석(요약 + 간단 인사이트)을 생성한다.
- [ ] 전세계 증시·경제 관련 뉴스(뉴스API + 주요 RSS)를 수집해 요약(추출 + abstractive 3문장) 제공한다.
- [ ] 알림/리포트는 Slack, 이메일, Telegram 채널로 전송 가능하다.
- [ ] 로그 및 메트릭(Prometheus)으로 이상 감지 및 재시도 정책을 운영한다.

**Out of scope (MVP):**
- 개인화된 포트폴리오(종목별 추천)
- 유료 데이터 피드 통합(예: Bloomberg 엔터프라이즈)
- 복잡한 머신-learning 예측 모델(버전 2로 이관)

**Key decisions (초기):**
- 데이터 소스: Yahoo Finance (무료) + Alpha Vantage (fallback). 뉴스: NewsAPI + 주요 경제지 RSS(FT, WSJ, Reuters).
- 인프라: Python FastAPI backend, Postgres for metadata, Redis for caching/alerts, Kubernetes 배포.
- 실시간 가격: Websocket 지원이 없다면 1분 폴링. 임계치 기반 알림 우선.
- 요약/분석: 초기는 LLM 기반 요약 엔진(자체 LLM 또는 OpenAI) 사용, 추후 자체 ML로 이관.
- 보안/규정: 뉴스/시장 데이터의 저작권 및 API 이용 약관 준수.

**Initial milestones:**
1. 스펙 + 이슈 생성 (현재)
2. 데이터 ingestion + Top10 scheduler (Marcus)
3. 가격 폴링 + alert engine (Marcus, Noah)
4. 뉴스 수집 + LLM 요약( Lisa )
5. Delivery channels: Slack, Email, Telegram (Kevin, Ryan)
6. QA + Runbooks (Dana, Noah)

**GitHub Issue:** #PLACEHOLDER
