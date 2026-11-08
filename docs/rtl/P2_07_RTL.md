# 제2부 07장 RTL 테크트리·모듈 동작 설명

> 근거: P2_01_to_10_Integrated_Review_20261106.zip. 소스 기반 교육용 도면이며 RTL_SIM_PASS, SYNTH_TIMING_PASS, BOARD_PASS를 의미하지 않습니다.

## 1. RTL 테크트리

- **선수·기존 기능** — 06장 초음파 안전 정보 재사용
- **이번 장 추가/재사용** — motor_controller FRESH/TRIP/DEADTIME
- **핵심 모듈·연결** — p2_07_axi_motor CMD/STATUS
- **출력·기능·안전** — motor_in1/motor_in2/motor_ena
- **검증 경계** — 물리 E-Stop·Watchdog 미구현

## 2. 모듈별 실제 입출력·제어 관계

### basys3_soc11_top

- 원본 파일: `basys3_soc11_top_p2_07.v`
- 기능 분류: 보드 Top (Shell/Wrapper)
- 처리 흐름:
  - **Basys3 보드 외부 포트** — clk·btnC·UART·SW·센서·출력 포트
  - **내부 wire 선언** — gpio_led / p2_led0 및 장별 연결선
  - **soc11_integration_wrapper** — Vivado BD 생성 포트와 실제 이름 대조
  - **LED 출력 결선** — LED0 IP / LED1 auto_light / LED2 Sonic / GPIO3~15
  - **보드 출력·안전** — Top 내부 FSM/계산 로직 없음
- 주의: Wrapper 미검증 포트는 실증 전 확인 필요

### motor_controller

- 원본 파일: `motor_controller.v`
- 기능 분류: 모터 인터록·TRIP·데드타임
- 처리 흐름:
  - **fresh_count** — 유효 sonic_done_i 때 FRESH_CYCLES 로드
  - **sensor_safe_o** — AUTO·FRESH·VALID·!UNSAFE
  - **trip_latched_o** — 구동 요청 중 unsafe → TRIP 래치
  - **drive_dir / dead_count** — STOP·반전 시 방향 OFF 및 DEADTIME
  - **motor_ena_o** — 조합 인터록 충족 시만 ENA 출력
- 주의: 독립 Watchdog·물리 E-Stop은 구현되지 않음.

### p2_07_axi_motor_v1_0

- 원본 파일: `p2_07_axi_motor_v1_0.v`
- 기능 분류: AXI IP 상위 Wrapper
- 처리 흐름:
  - **s00_axi_* 입력** — AW/W/B/AR/R · aclk/aresetn
  - **하위 S00_AXI 모듈** — p2_07_axi_motor_v1_0_S00_AXI 인스턴스 연결
  - **장치 데이터 경로** — Core 출력·IRQ·상태를 외부 포트로 전달
  - **연산 로직 경계** — 레지스터 디코드는 S00_AXI/Core에 위치
- 주의: 상위 IP Wrapper 자체의 추가 FSM은 없음

### p2_07_axi_motor_v1_0_S00_AXI

- 원본 파일: `p2_07_axi_motor_v1_0_S00_AXI.v`
- 기능 분류: AXI4-Lite 레지스터 Slave
- 처리 흐름:
  - **AW / W 독립 수신** — AWVALID·WVALID / 주소·데이터·WSTRB 래치
  - **쓰기 주소 디코드** — CMD STOP/FWD/REV(0x00) / STATUS(0x04)
  - **쓰기 응답 보존** — OKAY/SLVERR · BVALID은 BREADY까지 유지
  - **AR 읽기 수신** — ARVALID / ARADDR 별도 핸드셰이크
  - **읽기 데이터 선택** — CMD STOP/FWD/REV(0x00) / STATUS(0x04)
  - **읽기 응답 보존** — RDATA/RRESP/RVALID은 RREADY까지 유지
- 주의: STOP Clear 펄스·blocked/trip/deadtime 상태 읽기

## 3. 이전 장 유지 및 실증 경계

- `motor_controller`는 sensor_safe/fresh/trip/deadtime을 이용해 ENA를 차단합니다. 소프트웨어 STOP과 물리적 E-Stop은 동일하지 않습니다.
- 실제 비트스트림, BD/자동 생성 Wrapper, RTL testbench, Vitis BSP 및 실물 확인 증거는 이 설명 문서에 포함되지 않습니다.
- 기존 제1부 성공 프로젝트 및 C 명령 처리 플로우차트는 보존합니다.

- [장별 RTL 모듈 다중 페이지 JSON](../../chapters/P2_07_rtl_pages.json)

