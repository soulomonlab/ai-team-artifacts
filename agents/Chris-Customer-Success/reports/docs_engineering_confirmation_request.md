# Docs follow-up: 엔지니어링 확인 요청

요약
- Emma가 작성한 문서(output/docs/api_examples_update.md, output/docs/docs_pr_changes_summary.md)에 PR 머지 전 확인이 필요한 엔지니어링 항목이 있습니다.
- 제가 엔지니어링 확인을 받아 문서 PR을 마무리하도록 조치하겠습니다. 우선 Alex님 확인 요청드립니다.

확인이 필요한 항목 (핵심 질문)
1) widget.size 타입
   - 질문: widget.size는 number (정수/부동소수)로 할지, string(`"small"|"medium"|"large"`)으로 할지 확정 필요.
   - 영향: API 예제, 입력 검증, 클라이언트 라이브러리 타입 정의에 영향.

2) metadata 스키마
   - 질문: metadata는 자유 포맷(key-value JSON)으로 둘지, 사전 정의된 키 집합(schema)을 강제할지 결정 필요. (nullable 여부 포함)
   - 영향: API 참조 예시, 저장소 스키마, 검색/필터링 가능성.

3) status enum / soft-delete 동작
   - 질문: 리소스 상태는 enum(예: active, archived, deleted)로 처리할지, soft-delete를 별도 플래그(deleted: true)로 처리할지 확정 필요.
   - 영향: 삭제/복구 API, 목록 반환(기본값: deleted 포함 여부), 클라이언트 UX.

4) WIDGETS_CACHE_TTL 환경 변수
   - 질문: 기본값(초 단위)과 범위 제약(최소/최대)을 명시해야 함. 또한 단위(초/밀리초) 표기 통일 필요.
   - 영향: 런북(runbook) 문서, 배포 시 환경 변수 설정 가이드, 캐시 무효화 정책.

추가 컨텍스트
- 관련 파일: output/docs/api_examples_update.md, output/docs/docs_pr_changes_summary.md (Emma가 생성)
- Emma의 제안 작업: 엔지니어링 답변 확인 후 API 레퍼런스와 런북을 업데이트하고 docs PR을 생성 예정. Emma는 PR 초안 생성 후 엔지니어 태깅도 가능하다고 함.

요청사항 (Alex님께)
1) 위 4개 항목에 대해 최종 결정/권장안을 주시거나 Marcus에게 확인을 요청해 주세요.
2) PR 생성 방식 선택: (A) Emma가 PR 초안 생성 + 엔지니어 태깅 (권장, 빠른 병합) 또는 (B) 엔지니어 확인 후 Emma가 최종 커밋 (기본). 어떤 방식으로 진행할지 알려주세요.
3) 확인 결과를 주시면 제가 Emma에게 전달하고 문서 최종화/PR 오픈 진행하겠습니다.

제안(권장 기본값, 변경 가능)
- widget.size: string enum ('small'|'medium'|'large') — UI/UX 대응이 쉬워서 권장.
- metadata: 자유 포맷(JSON)지만, 검색용 주요 키(name, version)를 권장(문서에 명시).
- status: enum(active, archived, deleted) + deleted는 soft-delete로 구현(복구 가능).
- WIDGETS_CACHE_TTL: 기본값 300 (초), 최소 30, 최대 86400. 단위: 초로 문서화.

파일 위치
- output/reports/docs_engineering_confirmation_request.md (이 파일)

다음 단계
- Alex님 확인/지시를 기다린 후 Emma에게 전달하여 PR 오픈 또는 초안 생성 진행하겠습니다.
