# 제2부 02장 RTL 테크트리·모듈 동작 설명

> 근거: P2_01_to_10_Integrated_Review_20261106.zip. 실제 소스 기반의 교육용 설명이며 시뮬레이션·Vivado 합성 및 Basys3 실물 성공을 뜻하지 않습니다.

## 1. RTL 테크트리

- **선수·기존 기능** — 01장 LED0 유지
- **이번 장 추가/재사용** — p2_02_axi_fnd_v1_0 → S00_AXI
- **핵심 모듈·연결** — DISP_VALUE/CTRL 레지스터 → fnd_scan_controller
- **출력·기능·안전** — AN0~3·SEG·DP Active-Low
- **검증 경계** — 4자리 BCD 선행 0 및 프레임 갱신

## 2. 실제 RTL 모듈·입출력·기능

### basys3_soc11_top

- 원본 파일: `basys3_soc11_top_p2_02.v`
- 역할: 보드 Top (Shell/Wrapper)
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **Basys3 보드 외부 포트** — clk·btnC·UART·SW·센서·출력 포트
  - **내부 wire 선언** — gpio_led / p2_led0 및 장별 연결선
  - **soc11_integration_wrapper** — Vivado BD 생성 포트와 실제 이름 대조
  - **LED 출력 결선** — LED0 IP / LED1~15 GPIO
  - **보드 출력·안전** — Top 내부 FSM/계산 로직 없음
- 핵심 주의: Wrapper 미검증 포트는 실증 전 확인 필요

### fnd_scan_controller

- 원본 파일: `fnd_scan_controller.v`
- 역할: 4자리 FND 시분할 RTL Core
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **resetn / divider_count** — 리셋 시 scan_index·frame_bcd·enable 초기화
  - **divider_count 경계** — TICKS_PER_DIGIT마다 scan_index 0..3 순환
  - **frame_bcd 갱신** — scan_index=3 경계에서 4자리 값을 함께 래치
  - **current_digit 선택** — AN0은 [3:0], AN3은 [15:12]
  - **seg / an 출력** — 0..9 디코딩·Active-Low·DP OFF
- 핵심 주의: BCD 0050 선행 0 유지. 한 프레임 중 값 교체 방지.

### p2_02_axi_fnd_v1_0

- 원본 파일: `p2_02_axi_fnd_v1_0.v`
- 역할: AXI IP 상위 Wrapper
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **s00_axi_* 입력** — AW/W/B/AR/R · aclk/aresetn
  - **하위 S00_AXI 모듈** — p2_02_axi_fnd_v1_0_S00_AXI 인스턴스 연결
  - **장치 데이터 경로** — Core 출력·IRQ·상태를 외부 포트로 전달
  - **연산 로직 경계** — 레지스터 디코드는 S00_AXI/Core에 위치
- 핵심 주의: 상위 IP Wrapper 자체의 추가 FSM은 없음

### p2_02_axi_fnd_v1_0_S00_AXI

- 원본 파일: `p2_02_axi_fnd_v1_0_S00_AXI.v`
- 역할: AXI4-Lite 레지스터 Slave
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **AW / W 독립 수신** — AWVALID·WVALID / 주소·데이터·WSTRB 래치
  - **쓰기 주소 디코드** — DISP_VALUE(0x00) / DISP_CTRL(0x04)
  - **쓰기 응답 보존** — OKAY/SLVERR · BVALID은 BREADY까지 유지
  - **AR 읽기 수신** — ARVALID / ARADDR 별도 핸드셰이크
  - **읽기 데이터 선택** — DISP_VALUE(0x00) / DISP_CTRL(0x04)
  - **읽기 응답 보존** — RDATA/RRESP/RVALID은 RREADY까지 유지
- 핵심 주의: AW/W 독립 수신·WSTRB·예약 주소 SLVERR

## 3. 누적 검증 기준

- FND `fnd_scan_controller`의 `frame_bcd`는 프레임 경계에서 갱신하며, 0050의 선행 0을 유지합니다. AN/SEG는 Active-Low입니다.
- 이전 장 AXI IP, GPIO·IRQ·FND·PWM 등 유지 기능은 실제 BD/Wrapper와 연결 관계를 별도 대조합니다.
- 각 장의 RTL/AXI 시뮬레이션, 합성·타이밍·실물 동작은 미검증입니다.

- [RTL 모듈별 다중 페이지 JSON](../../chapters/P2_02_rtl_pages.json)
- 기존 C 명령 처리 도면은 변경하지 않았습니다.

