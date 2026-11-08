# 제2부 03장 RTL 테크트리·모듈 동작 설명

> 근거: P2_01_to_10_Integrated_Review_20261106.zip. 실제 소스 기반의 교육용 설명이며 시뮬레이션·Vivado 합성 및 Basys3 실물 성공을 뜻하지 않습니다.

## 1. RTL 테크트리

- **선수·기존 기능** — 01~02장 LED/FND 유지
- **이번 장 추가/재사용** — button_event_core 2FF·디바운스
- **핵심 모듈·연결** — PENDING/ENABLE/COALESCED AXI 레지스터
- **출력·기능·안전** — IRQ → AXI INTC (BD 연결 필요)
- **검증 경계** — BTNC Reset / BTNU·D·L·R 이벤트

## 2. 실제 RTL 모듈·입출력·기능

### basys3_soc11_top

- 원본 파일: `basys3_soc11_top_p2_03.v`
- 역할: 보드 Top (Shell/Wrapper)
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **Basys3 보드 외부 포트** — clk·btnC·UART·SW·센서·출력 포트
  - **내부 wire 선언** — gpio_led / p2_led0 및 장별 연결선
  - **soc11_integration_wrapper** — Vivado BD 생성 포트와 실제 이름 대조
  - **LED 출력 결선** — LED0 IP / LED1~15 GPIO
  - **보드 출력·안전** — Top 내부 FSM/계산 로직 없음
- 핵심 주의: Wrapper 미검증 포트는 실증 전 확인 필요

### button_event_core

- 원본 파일: `button_event_core.v`
- 역할: 버튼 동기화·Short/Long 이벤트
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **meta / synced** — btn_raw[k]를 2FF 동기화
  - **db_ticks** — DEBOUNCE_CYCLES 안정 시 debounced 갱신
  - **눌림 확정** — hold_ticks=0 / long_sent=0
  - **누름 유지** — LONG_CYCLES에서 event_pulse[k+4]
  - **해제 확정** — long_sent=0이면 event_pulse[k]
  - **pressed 출력** — 4개 버튼 각각 독립 상태 유지
- 핵심 주의: Short는 해제에서, Long은 보유 중 1회. BTN C는 Reset.

### p2_03_axi_buttons_v1_0

- 원본 파일: `p2_03_axi_buttons_v1_0.v`
- 역할: AXI IP 상위 Wrapper
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **s00_axi_* 입력** — AW/W/B/AR/R · aclk/aresetn
  - **하위 S00_AXI 모듈** — p2_03_axi_buttons_v1_0_S00_AXI 인스턴스 연결
  - **장치 데이터 경로** — Core 출력·상태·해당 시 IRQ 포트 연결
  - **연산 로직 경계** — 레지스터 디코드는 S00_AXI/Core에 위치
- 핵심 주의: 상위 IP Wrapper 자체의 추가 FSM은 없음

### p2_03_axi_buttons_v1_0_S00_AXI

- 원본 파일: `p2_03_axi_buttons_v1_0_S00_AXI.v`
- 역할: AXI4-Lite 레지스터 Slave
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **AW / W 독립 수신** — AWVALID·WVALID / 주소·데이터·WSTRB 래치
  - **쓰기 주소 디코드** — PENDING(0x00) / ENABLE(0x04) / COALESCED(0x10)
  - **쓰기 응답 보존** — OKAY/SLVERR · BVALID은 BREADY까지 유지
  - **AR 읽기 수신** — ARVALID / ARADDR 별도 핸드셰이크
  - **읽기 데이터 선택** — PENDING(0x00) / ENABLE(0x04) / COALESCED(0x10)
  - **읽기 응답 보존** — RDATA/RRESP/RVALID은 RREADY까지 유지
- 핵심 주의: W1C Clear, 같은 비트 Set 우선. irq=|(pending & enable_mask)

## 3. 누적 검증 기준

- `button_event_core`: Short는 디바운스 해제에서, Long은 누른 상태에서 1회만 발생합니다. `COALESCED`는 같은 종류의 중복 이벤트 플래그이며 정확한 횟수 카운터가 아닙니다.
- 이전 장 AXI IP, GPIO·IRQ·FND·PWM 등 유지 기능은 실제 BD/Wrapper와 연결 관계를 별도 대조합니다.
- 각 장의 RTL/AXI 시뮬레이션, 합성·타이밍·실물 동작은 미검증입니다.

- [RTL 모듈별 다중 페이지 JSON](../../chapters/P2_03_rtl_pages.json)
- 기존 C 명령 처리 도면은 변경하지 않았습니다.

