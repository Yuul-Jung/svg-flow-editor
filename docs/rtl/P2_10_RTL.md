# 제2부 10장 RTL 테크트리·모듈 동작 설명

> 근거: P2_01_to_10_Integrated_Review_20261106.zip. 소스 기반 교육용 도면이며 RTL_SIM_PASS, SYNTH_TIMING_PASS, BOARD_PASS를 의미하지 않습니다.

## 1. RTL 테크트리

- **선수·기존 기능** — 09장 사용자 RTL·IP 재사용
- **이번 장 추가/재사용** — motor_controller 하드웨어 안전 유지
- **핵심 모듈·연결** — RUN START/STOP/RESET은 Vitis C 정책
- **출력·기능·안전** — 기존 Top `basys3_soc11_top` 그대로
- **검증 경계** — 새 Watchdog / 물리 E-Stop 없음

## 2. 모듈별 실제 입출력·제어 관계

### basys3_soc11_top

- 원본 파일: `basys3_soc11_top_p2_08.v`
- 기능 분류: 보드 Top (Shell/Wrapper)
- 처리 흐름:
  - **Basys3 보드 외부 포트** — clk·btnC·UART·SW·센서·출력 포트
  - **내부 wire 선언** — gpio_led / p2_led0 및 장별 연결선
  - **soc11_integration_wrapper** — Vivado BD 생성 포트와 실제 이름 대조
  - **LED 출력 결선** — LED0 IP / LED1 auto_light / LED2 Sonic / GPIO3~15
  - **보드 출력·안전** — Top 내부 FSM/계산 로직 없음
- 주의: 08장의 Top 파일 그대로 재사용

## 3. 이전 장 유지 및 실증 경계

- 새 사용자 RTL 파일은 없습니다. RUN 상태 기계는 C 정책이며 HW motor_controller의 TRIP/Deadtime 제약을 유지합니다. 별도 Watchdog·물리 E-Stop 구현 없음.
- 실제 비트스트림, BD/자동 생성 Wrapper, RTL testbench, Vitis BSP 및 실물 확인 증거는 이 설명 문서에 포함되지 않습니다.
- 기존 제1부 성공 프로젝트 및 C 명령 처리 플로우차트는 보존합니다.

- [장별 RTL 모듈 다중 페이지 JSON](../../chapters/P2_10_rtl_pages.json)

