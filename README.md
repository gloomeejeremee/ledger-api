# ledger-api (클라우드컴퓨팅실습 4주차 과제)

- GitHub: https://github.com/gloomeejeremee/ledger-api
- Render: https://ledger-api-2y2q.onrender.com/docs

## 1. 결과 확인
<img width="1425" height="652" alt="스크린샷 2026-10-07 오후 4 34 22" src="https://github.com/user-attachments/assets/fbd9edbb-21cf-42d6-ba1f-5983dc336bc5" />
<img width="1389" height="639" alt="스크린샷 2026-10-07 오후 4 34 32" src="https://github.com/user-attachments/assets/26b9de2a-04b0-47c6-85b4-e725f95395f0" />
<img width="1437" height="631" alt="스크린샷 2026-10-07 오후 4 34 52" src="https://github.com/user-attachments/assets/a032bf45-e810-44c9-a3f9-12f2db5460ad" />
<img width="1419" height="650" alt="스크린샷 2026-10-07 오후 4 35 02" src="https://github.com/user-attachments/assets/de92ca37-9711-4ab9-92ac-4b085b6006b8" />

## 2. 핵심 개념
- **계좌와 거래를 두 테이블로 나눈 이유:** 계좌 하나에 거래가 여러 건 붙는 1:N 관계이기 때문이다. 거래는 계좌 정보를 복사하지 않고 `account_id`(외래키)로 계좌를 가리킨다. 그래서 계좌 이름을 바꿔도 한 곳만 고치면 되고, 존재하지 않는 계좌에 거래가 들어가는 일도 DB가 막아 준다.
- **모델 클래스와 실제 테이블의 대응:** `models.py`의 클래스 하나가 테이블 하나다(`Account` → `accounts`). 클래스 속성이 열이 되고, `Mapped[str | None]`처럼 쓴 타입이 NULL 허용 여부 같은 제약 조건이 된다. 앱이 시작될 때 `create_all()`이 이 정의를 보고 `CREATE TABLE`을 대신 실행한다.
- **연결 문자열을 .env로 분리하는 이유:** 연결 문자열 안에 DB 비밀번호가 들어 있기 때문이다. 코드에 직접 쓰면 GitHub에 그대로 공개되므로, `.env`(로컬)나 Render 환경변수(배포)에 따로 두고 `.gitignore`로 Git에서 제외한다. 코드는 `os.getenv("DATABASE_URL")`로 읽기만 하니, 환경이 바뀌어도 코드는 그대로 두고 값만 바꾸면 된다.

## 3. 자유 로그
- 수업 중 실습을 따라가지 못해서, 수업 후 워크북 단계 2~5를 처음부터 다시 진행했다. 로컬 실행은 건너뛰고 Render 배포 결과로 바로 검증했다.
- Supabase 화면이 워크북과 달라서 Session pooler 위치를 찾는 데 시간이 걸렸다. **Connect → Direct(Connection string)** 탭에서 Method를 바꾸면 나왔다.
- 첫 배포는 `password authentication failed`로 실패했다. 두 번째는 `tenant/user postgres.abcdefgh not found`로 실패했는데, 설명용 예시 문자열의 ref를 그대로 넣은 것이 원인이었다. 실제 프로젝트 ref(`postgres.<ref>`)와 비밀번호로 고친 뒤 배포에 성공했다. 사용자명이 `postgres`가 아니라 `postgres.<프로젝트ref>`라는 점, 오류 메시지가 인증 실패인지 사용자 못 찾음인지에 따라 원인이 다르다는 점을 배웠다.
- 배포 주소에 처음 들어가면 `{"detail":"Not Found"}`가 떠서 실패한 줄 알았다. 그런데 이건 `/` 경로가 없어서 나오는 FastAPI의 정상 응답이었고, `/docs`로 들어가야 했다.
- **AI 활용과 검증:** Claude에게 워크북 단계 5의 진행 순서 정리, 코드 파일 생성 명령, Render 오류 로그 해석을 요청했다. 결과는 세 가지로 검증했다. ① Render 로그에서 오류 문구가 사라지고 서비스가 Live가 되는지, ② `/docs`에서 POST·GET 응답 코드(201/200)와 값이 맞는지, ③ Supabase Table Editor에 같은 행이 실제로 생겼는지.
- 아직 안 해 본 것: 로컬에서 `uvicorn`으로 직접 실행하기, 확장 단계(Alembic, 트랜잭션)
