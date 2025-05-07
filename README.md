# 🧪 Django 기반 서버 시뮬레이터

> API 시나리오 기반 부하 테스트 및 가상 유저 시뮬레이션 플랫폼  
> (Scenario-based Load Testing & Virtual User Simulation)

---

## 🔍 소개

이 프로젝트는 시뮬레이션 가능한 서버 부하 테스트 플랫폼입니다.  
사용자는 API 시나리오를 정의하고, 해당 시나리오를 여러 가상 유저(`Sim`)로 실행하거나 부하 테스트(`LoadTest`)로 병렬 요청을 보낼 수 있습니다.  
향후 결과 리포트 시각화 기능까지 확장 가능합니다.

---

## 🗂️ Django 앱 구성

| 앱 이름 | 설명 |
|--------|------|
| **`scenario`** | 🧩 시나리오 및 API 스텝 정의<br>순서 지정 및 의존 관계 설정 가능 |
| **`simulator`** | 👥 가상 유저 생성 및 실행<br>시나리오 실행, 부하 테스트 트리거 |
| **`notification`** | 📬 알림 템플릿 관리 및 전송<br>SMS, 알림톡, 메일 지원 예정 |
| **`report`** | 📊 결과 리포트 및 시각화 (개발 예정) |
| **`common`** | 🧰 공통 Mixin, 유틸, 예외 처리 등 공유 코드 |

---

## 🚀 주요 기능

### ✅ 시나리오 관리

- 여러 API 호출을 순서대로 구성하여 시나리오 생성
- 스텝 간 의존 관계(선행 Step 설정) 가능
- 반복 가능하거나 조건 분기형 로직도 지원 예정

### ✅ 가상 유저 실행

- `Sim` 유저 생성 후, 시나리오를 병렬 실행
- 가상의 인증/요청 처리 로직 포함 가능

### ✅ 부하 테스트

- `LoadTest` 정의 후, 특정 endpoint에 N명 사용자로 burst 요청
- method, body, headers, concurrency 수치 설정 가능
- (예정) 실제 응답 시간/성공률 기록 및 리포트

### ✅ 알림 시스템

- 메시지 템플릿 등록 및 관리
- 다수 유저 대상 알림 발송 처리 지원

---

## 📌 API 사용 예시

### 시나리오 관련
```http
POST   /api/scenarios/                     → 시나리오 생성
POST   /api/scenarios/with-steps/         → 스텝 포함 생성
POST   /api/scenarios/{id}/executions/    → 시나리오 실행
