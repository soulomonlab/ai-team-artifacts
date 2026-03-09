목표
- 모바일(안드로이드/iOS)에서 핵심 기능을 기기 내(on-device)에서 실행하는 POC를 만들고, 레이턴시(latency), 메모리, CPU 사용량을 측정하여 통합 절차를 제시한다.

성공 기준
- 단일 추론(단일 입력 → 출력) 평균 레이턴시: 목표 < 200ms (저사양 기기에서는 단계적 완화)
- 메모리: 추가 런타임 메모리 증가 < 50MB
- CPU: 연속 추론(초당 1~5회) 시 UI 병목 없음(60fps 유지 우선권)
- 통합 가이드: Android(TFLite), iOS(CoreML) 통합 단계 문서화

제약 조건
- 모델 포맷: TensorFlow Lite(.tflite) 우선권(안드로이드), CoreML(.mlmodel) 우선권(iOS)
- 앱 번들 크기 증가: 모델 파일 크기 < 10MB 권장(업데이트 전략 필요)
- 네이티브 의존성 추가(라이브러리) 허용

설계 옵션(단순화)
1) TFLite 모바일 런타임 (안드로이드) + CoreML (iOS)
   - 장점: 런타임 최적화 지원, 양 플랫폼 네이티브 성능
   - 단점: 두 포맷/파이프라인 유지 비용
2) ONNX Runtime Mobile (양 플랫폼 통일)
   - 장점: 모델 파이프라인 단일화
   - 단점: 런타임 크기 + 통합 난이도

결정(근거)
- POC 단계에서는 개발 편의성과 커뮤니티 플러그인(React Native) 가용성을 고려하여
  Android: TFLite(.tflite)
  iOS: CoreML(.mlmodel)
  로 진행. 추후 ONNX로 통합 전환 검토.

측정 지표
- 레이턴시: cold start(앱 재시작 후 첫 추론), warm path(연속 추론)
- 메모리: 전체 프로세스 메모리 변화(dumpsys / Instruments)
- CPU: 평균 및 피크 사용률(Profiler)
- 전력(옵션): 배터리 소비 추정(샘플 1분간 연속 추론)

테스트 디바이스(권장)
- 저사양 Android: Android 8.1, 2GB RAM
- 중상급 Android: Android 12, 6GB RAM
- iOS 저사양: iPhone 8 / iOS 14
- 최신 iOS: iPhone 13 / iOS 16

POC 산출물
- sample React Native wrapper + demo screen (output/code/poc/InAppInference.tsx)
- 네이티브 통합 가이드(Android / iOS)
- 벤치마크 실행 스크립트 및 측정 가이드
- 결과 기록 템플릿

리스크 및 다음 단계
- 모델이 .tflite/.mlmodel로 바로 제공되지 않는 경우: 백엔드(Marcus)에서 변환 필요
- 모델 파일이 클 경우: 앱 번들이 아닌 런타임 다운로드 전략 필요(DevOps 협의)
