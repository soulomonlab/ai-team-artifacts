# Austria Guide App — Wireframes & User Flows (MVP)

요약
- 목적: PRD(output/specs/austria_guide.md)에 따른 MVP용 모바일/웹(React + React Native) 디자인 산출물.
- 산출물: 주요 화면의 와이어프레임(ASCII), 사용자 흐름, 화면 체크리스트, 핵심 상호작용(지도/POI/여정), 퍼스트-파스 컴포넌트 제안.

타겟 유저/시나리오 (간단)
- 관광객(여행 전/중): 간단히 도시 검색 → POI 확인 → 여정에 추가 → 공유
- 현지 사용자(빠른 길찾기): 검색 → 지도에서 POI 확인 → 길안내(외부 앱)

핵심 가정/제약
- 지도는 벡터 타일 + MBTiles을 사용(오프라인 가능성 표시 필요).
- GDPR: 분석은 옵트-인. 초기 UX에 옵트-인 플로우 포함.
- React Native 우선 모바일 레이아웃 중심. 데스크탑은 확장성 고려.

화면 체크리스트 (필수, Figma 파일에 각 화면 프레임 포함)
1. Home (목표, 추천 도시, 검색 입력, 최근/저장된 여정)
2. City page (개요, 지도 미니뷰, 인기 POI 리스트, 카테고리 필터)
3. POI detail (카드 / 바텀시트 + 전체화면, 사진, 설명, 주소, 오픈시간, 연락처, 길찾기, 즐겨찾기)
4. Search results (쿼리 입력, 필터, 결과 리스트, 지도 토글)
5. Map view (전체 지도, POI 마커, 클러스터, 현재위치, 오프라인 상태)
6. Itinerary editor (타임라인, POI 추가/삭제/순서변경, 저장/공유)
7. Share modal (링크/소셜, 권한, 복사)
8. Onboarding/GDPR opt-in modal (분석 동의)
9. Settings (언어, 데이터 / 오프라인 맵 관리)

사용자 흐름 (요약)
A. 기본 탐색
- Home -> 검색 또는 추천 도시 선택 -> City page -> POI 선택 -> POI detail -> (+) 추가 -> Itinerary -> 저장/공유

B. 빠른 검색
- 탑바 검색 아이콘 탭 -> Search -> 입력 -> 실시간 결과 -> 결과 선택 -> POI detail

C. 오프라인/지도 중심
- Home -> Map view -> 위치 권한 허용 -> 마커 탭 -> POI 바텀시트 오픈 -> 저장 또는 길찾기

와이어프레임 (모바일 중심, ASCII)

1) Home (mobile 375x812)
----------------------------------------
| Header: [≡]   Austria Guide    [🔔] |
----------------------------------------
| Search bar (place: 'Search city, POI...')|
| [Recent searches chips]                 |
----------------------------------------
| Featured Cities (horizontal cards)     >|
| [Vienna] [Salzburg] [Innsbruck]       |
----------------------------------------
| Nearby / Recommended (vertical list)   |
| • Schönbrunn Palace  — 4.8 ⭐ — 1.2 km  |
| • St. Stephen's Cathedral — 3.5 km      |
----------------------------------------
| Bottom Nav: [Home][Map][Itinerary][Profile] |
----------------------------------------

Interaction notes:
- City 카드: 이미지 왼쪽, 도시명+국제 아이콘, tap -> City page.
- Search: onFocus -> open Search screen (full screen) with history.

2) City page
----------------------------------------
| Back | Vienna                       [★save] |
----------------------------------------
| Map mini (tap to open full map)                |
| [Map preview]                                  |
----------------------------------------
| Tabs: Overview | POIs | Map                     |
----------------------------------------
| POI List (card per row)                         |
| • Schönbrunn Palace  — museum — 30 min visit    |
|   [photo] [save][share]                         |
----------------------------------------

Interaction: POI tap -> POI detail (bottom sheet slide up)

3) POI Detail (Bottom Sheet / Full)
----------------------------------------
| Handle (drag)                                   |
| Title: Schönbrunn Palace   [⭐4.8] [save] [share]|
| Image carousel                                   |
| Short description                                |
| Info row: [Open hours] [Address] [Phone] [WWW]   |
| Buttons: [Directions] [Add to Itinerary]         |
----------------------------------------
| Reviews (collapsed)                              |
----------------------------------------

Notes: Bottom sheet supports two states: peek (mini) and expanded (full). Include deep link share.

4) Search Results
----------------------------------------
| Back | Search query                             |
----------------------------------------
| Filters: [All][Museums][Parks][Food] [Nearby]    |
----------------------------------------
| Results list (with small map preview toggle)     |
| • Name — distance — tag(s)                       |
| (Empty state: suggest top results or popular POIs)|
----------------------------------------

5) Itinerary Editor
----------------------------------------
| Back | My Itinerary — "Vienna Day 1" [Save]    |
----------------------------------------
| Timeline:                                       |
| 09:00 — Schönbrunn Palace [▶︎ edit] [del]        |
| 12:00 — Lunch @ Naschmarkt                        |
| 14:00 — St. Stephen's Cathedral                  |
----------------------------------------
| Map strip with POI pins for itinerary            |
| Buttons: [Share] [Export (Google Maps)]          |
----------------------------------------

Interaction: drag handle on timeline items to reorder; show travel time estimate between items.

접근성 & 제약
- 터치 타겟: 최소 44x44px
- 색 대비: 텍스트와 배경 최소 4.5:1 (본문), 3:1(대형텍스트)
- 폰트 크기: 모바일 본문 16sp 권장

디자이너 결정 이유 (요약)
- 바텀시트: POI 세부정보는 컨텍스트 전환을 줄이기 위해 바텀시트 우선
- 지도 미니뷰: 화면 전환 감소, 빠른 탐색 가능
- 타임라인 편집: 드래그로 직관적 순서 변경

다음 행동(POC)
- Figma에 위 프레임(각 화면) 생성 후 공유 링크 전달
- 컴포넌트(카드, 버튼, 바텀시트) 토큰화 및 스타일 가이드 분리

파일: output/design/austria_guide_wireframes.md
