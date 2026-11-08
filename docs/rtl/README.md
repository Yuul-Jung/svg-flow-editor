# 제2부 01~10장 RTL 모듈별 테크트리 및 플로우차트

자료 출처: `P2_01_to_10_Integrated_Review_20261106.zip`의 실제 RTL Verilog 소스.

## 이용 방법

편집기에서 **도면 종류 → RTL 모듈별 → 원하는 장 열기**를 선택합니다. 각 장 첫 페이지는 RTL 테크트리, 이후 페이지는 해당 장 RTL 소스 파일별 기능 설명입니다.

| 장 | 주제 | RTL 페이지 | 설명 문서 | 다중 페이지 JSON |
|---|---|---:|---|---|
| 01 | 사용자 AXI LED0·Top | 2 | [01장 설명](./P2_01_RTL.md) | [RTL 도면](../../chapters/P2_01_rtl_pages.json) |
| 02 | FND 4자리 | 5 | [02장 설명](./P2_02_RTL.md) | [RTL 도면](../../chapters/P2_02_rtl_pages.json) |
| 03 | 버튼·IRQ | 5 | [03장 설명](./P2_03_RTL.md) | [RTL 도면](../../chapters/P2_03_rtl_pages.json) |
| 04 | PWM | 5 | [04장 설명](./P2_04_RTL.md) | [RTL 도면](../../chapters/P2_04_rtl_pages.json) |
| 05 | CdS 디지털·자동 조명 | 9 | [05장 설명](./P2_05_RTL.md) | [RTL 도면](../../chapters/P2_05_rtl_pages.json) |
| 06 | 초음파 | 5 | [06장 설명](./P2_06_RTL.md) | [RTL 도면](../../chapters/P2_06_rtl_pages.json) |
| 07 | 모터 안전 인터록 | 5 | [07장 설명](./P2_07_RTL.md) | [RTL 도면](../../chapters/P2_07_rtl_pages.json) |
| 08 | XADC Wizard | 2 | [08장 설명](./P2_08_RTL.md) | [RTL 도면](../../chapters/P2_08_rtl_pages.json) |
| 09 | MODE·Timer IRQ | 2 | [09장 설명](./P2_09_RTL.md) | [RTL 도면](../../chapters/P2_09_rtl_pages.json) |
| 10 | RUN 종합 | 2 | [10장 설명](./P2_10_RTL.md) | [RTL 도면](../../chapters/P2_10_rtl_pages.json) |

## 구현과 검증의 구분

- 01장의 AXI LED Wizard 생성 RTL 원본은 ZIP에 없으며 패치 지침만 제공됩니다.
- 05장의 PWM 코어 및 AXI 관련 3개 파일은 04장 원본과 동일하여 재사용으로 분류합니다.
- 08장은 XADC Wizard 제공 IP와 VAUX6 연결용 Top만 추가됩니다.
- 09~10장은 08장 Top을 재사용하며 신규 사용자 RTL은 없습니다. MODE/RUN 상태 처리는 소프트웨어 정책입니다.
- 장별 구조도는 소스 기반 교육용이며 RTL_SIM_PASS, SYNTH_TIMING_PASS, BOARD_PASS를 뜻하지 않습니다.
- 기존 C 명령 플로우차트 및 제1부 성공 프로젝트는 변경하지 않습니다.
