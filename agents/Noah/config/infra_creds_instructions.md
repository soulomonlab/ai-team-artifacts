# Dev infra credentials & vulnerability scanning — instructions

요약
- 목적: 개발(dev) 환경용 Postgres, Redis, CI 테스트 DB 리소스 프로비저닝 및 CI에 필요한 서비스 계정/자격증명 안전하게 저장(및 회전), GitHub 기반 취약점 스캐닝(Dependabot / Snyk) 연동 가이드 제공
- 산출물: 이 문서 (output/config/infra_creds_instructions.md)
- Acceptance criteria 충족: Vault/GitHub Actions에 비밀번호/키 저장법, 비밀명 명시, 회전 정책, 스캐닝 연동 절차 포함

상황 (Situation)
- 백엔드 CI가 dev 리소스(Postgres, Redis, CI 테스트 DB)에 접근해야 하며, 최소 권한 원칙(Least privilege)을 만족해야 함.
- 또한 의존성 취약점 자동 스캐닝(Dependabot 또는 Snyk)을 통해 보안 리스크를 사전에 탐지해야 함.

복잡성 (Complication)
- 서비스 계정 권한이 과도하면 보안 리스크, 부족하면 CI 파이프라인 실패.
- 자격증명을 코드/레포에 노출할 수 없고, 회전 정책이 필요.
- Snyk/GitHub 연동은 앱 설치/권한 부여 단계가 필요하고, 조직 정책상 수동 허가가 필요할 수 있음.

해결안(Resolution) — 요약된 액션 아이템
1) 리소스 선택(권장): AWS 기반으로 예시 제공(Cloud-agnostic 옵션 포함).
2) CI 전용 서비스 계정 생성(최소 권한) + 자격증명 Vault 및 GitHub Secrets에 등록.
3) 비밀 이름/경로 표준화 및 회전 정책 문서화.
4) Dependabot 설정 파일(.github/dependabot.yml) 추가 가이드 + Snyk 연동 방법(앱 설치 및 토큰 저장).
5) 수동 확인 항목 및 Acceptance checklist 제공.

세부 지침

1) 권장 프로비저닝(예시: AWS)
- Postgres (dev): RDS PostgreSQL, db.t3.micro (dev), 다중 AZ 불필요 (비용 절감). 네트워크: private subnet, SG는 CI runner IP / VPC peering만 허용.
- Redis (dev): ElastiCache Redis (single-node / t3.micro 작게 시작). 비밀번호(auth) 사용.
- CI 테스트 DB: 동일 RDS 인스턴스 내 별 DB 스키마 또는 별 RDS 인스턴스(격리 필요 시). CI 전용 DB는 "ci_db"로 생성.

Terraform(권장): 각 리소스는 Terraform으로 관리하세요. 예시 작은 아이디어:
- modules/db/aws_rds.tf (생성)
- modules/cache/aws_elasticache.tf
- outputs: rds_endpoint, rds_port, rds_dns

2) CI 서비스 계정/사용자(최소 권한)
- 목적: CI가 테스트 DB에 스키마 생성/마이그레이션/테스트 데이터 로드 가능해야 함.
- 권한 제안 (Postgres): Create DB, Connect, Create schema, DDL/DML (테스트 환경에서만). 운영 DB 권한과 분리.
- 권한 제안 (Redis): AUTH 비밀번호로 접근(모든 키 접근 허용 — 테스트 환경이므로 허용) 또는 ACL 사용(Redis >= 6).

AWS IAM(예시) - 만약 앱이 AWS 자원 생성/관리 필요시
- CI 서비스 계정(프로그램적 접근용): 최소 정책 예
  - rds-db:connect (특정 DB 리소스 ARN에만)
  - ssm:GetParameters (if using Parameter Store)
  - secretsmanager:GetSecretValue (if using Secrets Manager)
- 대신 HashiCorp Vault + AWS IAM auth backend로 동적 인증을 권장.

3) 자격증명 저장 위치 및 비밀 이름 표준
- Vault 경로(예시, HashiCorp Vault kv v2):
  - secret/data/dev/postgres/ci
     - fields: username, password, host, port, database
  - secret/data/dev/redis/ci
     - fields: password, host, port
  - secret/data/dev/service-accounts/ci
     - fields: key (JSON 또는 token), issued_at

- GitHub Actions Secrets(이름 권장):
  - DEV_POSTGRES_URL -> postgresql://ci_user:<password>@<host>:<port>/ci_db
  - DEV_REDIS_URL -> redis://:<password>@<host>:<port>
  - CI_SERVICE_ACCOUNT_KEY -> base64 또는 JSON 형태의 서비스 계정 키(짧게 유효한 토큰 권장)
  - SNYK_TOKEN -> (Snyk 연동용, if using Snyk API token)

- .env.example 파일 샘플 키 (레포에 포함, 실제 값은 NO):
  - DEV_POSTGRES_URL=
  - DEV_REDIS_URL=
  - CI_SERVICE_ACCOUNT_KEY=

참고: Vault 우선 사용 권장. GitHub Secrets은 배포 시 런타임 사용(읽기 전용)으로 제한.

4) Vault에 자격증명 등록 예시 명령
- (Vault kv v2) 예: vault kv put secret/dev/postgres/ci username=ci_user password=SuperSecret host=db.dev.example.com port=5432 database=ci_db
- GitHub Action에서 Vault 읽기: GH Action용 Vault 토큰을 사용하거나 Vault를 통해 short-lived token을 발급.

5) 회전 정책 (권장)
- DB admin/instance passwords: 90일 회전
- CI 서비스 계정 키 / tokens: 30일 회전(또는 short-lived 토큰 사용 권장)
- Redis AUTH: 90일 회전
- 자동화 권장: Vault dynamic secrets(가능하면 DB secrets engine 사용 — Vault가 필요 시 DB 계정 자동 생성/회전)
- 회전 시 체크리스트: CI 파이프라인에 새 비밀 적용 확인 -> smoke tests 실행

회전 절차(간단)
1. Vault에 새 비밀 삽입 (kv v2 put)
2. GitHub Secrets(필요 시) 업데이트
3. CI 파이프라인에서 smoke test 실행(health-check endpoint 사용 권장)
4. 이전 비밀 만료(7일 grace) 이후 삭제

6) Dependabot 설정(.github/dependabot.yml)
- Dependabot 파일 예시 (의존성 업데이트 및 security updates 활성화):

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 5
    allow:
      - dependency-type: "all"
```

- Repo settings에서 "Dependabot alerts" 및 "Dependabot security updates" 활성화 확인.

7) Snyk 연동 절차 (조직/리포 권한 필요)
- 설치: https://github.com/apps/snyk 인스톨 (Organization 레벨에서 설치 권장)
- 권한: repo contents 읽기 및 PR 생성 권한 부여 필요
- 토큰: Snyk 계정에서 API token 생성 -> GitHub Secret SNYK_TOKEN에 저장
- CI에서 실행: `snyk test` 및 `snyk monitor`를 CI 워크플로(예: GitHub Actions)에 추가
- 권장: PR 차단 정책 설정(critical/high vulnerability 발견 시 blocker 설정은 팀 합의 필요)

8) 최소 권한 원칙 적용 시 고려사항
- CI 서비스 계정은 프로덕션 리소스에 접근 불가하도록 강제(네트워크 레벨 + IAM 정책으로 차단)
- 개발용 DB/캐시와 운영용 리소스 별도 계정 사용

9) Acceptance checklist (검증기준)
- [ ] Vault에 다음 엔트리 존재: secret/data/dev/postgres/ci, secret/data/dev/redis/ci, secret/data/dev/service-accounts/ci
- [ ] GitHub Secrets에: DEV_POSTGRES_URL, DEV_REDIS_URL, CI_SERVICE_ACCOUNT_KEY, (SNYK_TOKEN if used)
- [ ] dependabot.yml가 레포에 추가되어 있고, Repo 설정에서 Dependabot 활성화됨
- [ ] Snyk 앱이 조직/레포에 설치되어 있거나 Snyk 사용 불가 시 연동 설치 방법 문서화됨
- [ ] Rotation policy 문서화(위의 주기) 및 소유자(contact person) 지정

10) 권한 위임/담당자
- Vault 관리자: Isabella (#ai-security) — 접근 제어 심사 필요
- CI 파이프라인 적용: Marcus (#ai-backend) — 액세스하여 워크플로에 Secrets를 추가하고, CI에서 DB/Redis 접속 검증 필요

11) 권장 자동화(향후 작업)
- Terraform으로 Vault secret bootstrap 스크립트 작성
- Vault DB secrets engine 도입 (dynamic DB creds)
- CI에서 Snyk/Dependabot 결과를 PR 코멘트 또는 Slack 알림으로 통합
- 회전 자동화: Vault + Lambda/CRON으로 주기적 비밀 교체 및 CI 재적용

부록: 예시 명령 모음
- Vault에 Postgres credential 추가
  vault kv put secret/dev/postgres/ci username=ci_user password=ChangeMe host=db.dev.internal port=5432 database=ci_db

- GitHub Secret 생성(gh CLI 사용 예)
  gh secret set DEV_POSTGRES_URL --body "postgresql://ci_user:ChangeMe@db.dev.internal:5432/ci_db"

- Dependabot 파일 생성
  mkdir -p .github && cat > .github/dependabot.yml <<EOF
  version: 2
  updates:
    - package-ecosystem: "pip"
      directory: "/"
      schedule:
        interval: "daily"
      open-pull-requests-limit: 5
EOF

검증 및 다음 단계
- 제가 Vault 경로 및 비밀 이름 표준을 문서화했습니다. (이 파일 참조)
- 다음 담당자 Marcus님(#ai-backend): 이 문서 기준으로 GitHub Action에 Secrets 추가하고, CI에서 실제로 DB/Redis 연결 테스트를 수행해 주세요.

문의 / 책임자
- 작성: Noah (DevOps)
- 보안 검토: Isabella (#ai-security)
- 백엔드 CI 적용: Marcus (#ai-backend)


