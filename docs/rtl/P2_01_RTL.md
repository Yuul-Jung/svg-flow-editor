# 제2부 01장 RTL 테크트리·모듈 동작 설명

> 근거: P2_01_to_10_Integrated_Review_20261106.zip. 실제 소스 기반의 교육용 설명이며 시뮬레이션·Vivado 합성 및 Basys3 실물 성공을 뜻하지 않습니다.

## 1. RTL 테크트리

- **선수·기존 기능** — 기존 MicroBlaze V SoC · UART/GPIO
- **이번 장 추가/재사용** — Vivado 생성 AXI LED IP 수정 지침
- **핵심 모듈·연결** — slv_reg0[0] → LED0 출력 배선
- **출력·기능·안전** — Top: LED[15:1] GPIO / LED0 IP
- **검증 경계** — AXI LED 전체 생성 RTL은 ZIP에 없음

## 2. 실제 RTL 모듈·입출력·기능

### basys3_soc11_top

- 원본 파일: `P2_01_basys3_top.v`
- 역할: 보드 Top (Shell/Wrapper)
- 동작 경로(회로 데이터/제어 관계; CPU의 순차 실행은 아님):
  - **Basys3 보드 외부 포트** — clk·btnC·UART·SW·센서·출력 포트
  - **내부 wire 선언** — gpio_led / p2_led0 및 장별 연결선
  - **soc11_integration_wrapper** — Vivado BD 생성 포트와 실제 이름 대조
  - **LED 출력 결선** — LED0 IP / LED1~15 GPIO
  - **보드 출력·안전** — Top 내부 FSM/계산 로직 없음
- 핵심 주의: Wrapper 미검증 포트는 실증 전 확인 필요

## 3. 누적 검증 기준

- AXI LED IP는 원본 ZIP에 Vivado 생성 RTL 완성본이 없고 `P2_01_AXI_RTL_Patch.md` 수정 지침만 있습니다. 따라서 AXI LED 내부 FSM이나 레지스터 RTL을 성공/완성으로 표시하지 않습니다.
- 이전 장 AXI IP, GPIO·IRQ·FND·PWM 등 유지 기능은 실제 BD/Wrapper와 연결 관계를 별도 대조합니다.
- 각 장의 RTL/AXI 시뮬레이션, 합성·타이밍·실물 동작은 미검증입니다.

- [RTL 모듈별 다중 페이지 JSON](../../chapters/P2_01_rtl_pages.json)
- 기존 C 명령 처리 도면은 변경하지 않았습니다.

