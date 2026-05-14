---
title: "Nursing XR Design System Principles"
company: "Nursing XR"
version: "v1.0"
date: "2026-05-14"
purpose:
  - Japan Exhibition Brochure
  - Singapore Medical Fair Asia Materials
  - IR Deck
  - One-Pager
  - Website Brand System
tags:
  - NursingXR
  - DesignSystem
  - BrandIdentity
  - HealthcareEdTech
  - IR
  - Exhibition
---

# Nursing XR Design System Principles  
## Purple-Led Clinical Healthcare EdTech Design

---

## 1. Core Design Direction

Nursing XR의 디자인은 단순한 기술 기업 이미지가 아니라, AI 기반 헬스케어 교육 기업으로서의 전문성, 신뢰성, 돌봄의 가치를 동시에 전달해야 한다.

### Design Statement

> White-based, purple-led, clinically trustworthy, human-centered AI healthcare education design.

### 국문 해석

> 흰 배경을 기반으로 보라색을 주조색으로 사용하며, 의료적 신뢰감과 인간중심 돌봄 가치를 함께 전달하는 AI 헬스케어 교육 디자인.

---

## 2. Brand Personality

| 요소 | 방향 |
|---|---|
| Core Identity | AI-powered healthcare learning system |
| Emotional Tone | 따뜻한 돌봄, 신뢰, 진정성 |
| Visual Tone | 전문적, 정돈된, 글로벌 B2B |
| Technical Tone | AI, 3D/VR, 시뮬레이션, 데이터 기반 학습 |
| Market Tone | 일본·싱가포르·글로벌 전시회에 적합한 신뢰형 디자인 |
| Avoided Impression | 게임형 VR 업체, 과장된 AI 스타트업, 과도한 네온 메타버스 기업 |

---

## 3. Color System

Nursing XR의 주조색은 보라색 계열로 유지한다.  
디자인은 흰 배경과 라벤더 계열의 부드러운 보조색을 활용하여 의료·교육 분야의 신뢰감을 유지한다.

### Primary Palette

| Role | Color Name | HEX | Usage |
|---|---|---|---|
| Primary | Nursing XR Purple | `#7132F5` | 핵심 CTA, 브랜드 포인트, 중요 키워드 |
| Secondary | Trust Purple | `#5741D8` | 버튼 테두리, 제목 강조, 다이어그램 포인트 |
| Deep Accent | Clinical Violet | `#5B1ECF` | 강조 배경, 그래픽 포인트 |
| Soft Surface | Soft Lavender | `#F4F0FF` | 섹션 배경, 카드 강조 영역 |
| Text Primary | Near Black | `#101114` | 주요 제목, 본문 핵심 텍스트 |
| Text Secondary | Cool Gray | `#686B82` | 보조 설명, 캡션 |
| Muted Text | Silver Gray | `#9497A9` | 주석, 보조 UI 텍스트 |
| Border | Border Gray | `#DEDEE5` | 카드 경계, 구분선 |
| Healthcare Accent | Clinical Blue | `#EAF3FF` | 의료·시뮬레이션 보조 배경 |
| Positive Accent | Care Green | `#149E61` | 성과, 개선, 긍정 지표 |

---

## 4. Colors to Avoid

사용자 선호에 따라 주황색 계열은 Nursing XR 디자인에서 사용하지 않는다.

| Avoided Color | Reason |
|---|---|
| Orange | 사용자가 선호하지 않음 |
| Yellow-Orange | 주황색 인상 가능 |
| Coral | 주황 계열로 보일 수 있음 |
| Peach | 따뜻하지만 주황빛으로 인식 가능 |
| Orange-Beige | 전체 톤이 주황색처럼 보일 위험 |
| Neon Orange | 의료·교육 신뢰감과 맞지 않음 |

### Design Rule

> Nursing XR 디자인에서는 주황색을 CTA, 강조색, 배경색, 아이콘색으로 사용하지 않는다.

---

## 5. Typography

Nursing XR은 한국어·영어·일본어 자료를 함께 사용하므로 다국어 호환성이 좋은 서체 체계가 필요하다.

| Language / Use | Recommended Font |
|---|---|
| Korean | Pretendard |
| English | Pretendard, Inter, IBM Plex Sans |
| Japanese | Noto Sans JP |
| Fallback | Helvetica, Arial, sans-serif |


---

## 5-1. Final Font Decision: Pretendard as Primary Typeface

Nursing XR의 전시회 브로슈어, 회사소개서, IR 자료, 웹사이트, 제안서 디자인에서는 Pretendard를 기본 서체로 사용한다.

### Font System Rule

```css
font-family: "Pretendard", "Noto Sans JP", "Inter", "Helvetica Neue", Arial, sans-serif;
```

### Recommended Font Application

| Area | Recommended Font Weight |
|---|---|
| Hero Title | Pretendard ExtraBold / Bold |
| Main Section Title | Pretendard Bold |
| Sub-heading | Pretendard SemiBold |
| Body Text | Pretendard Regular / Medium |
| Badge / CTA | Pretendard SemiBold |
| Japanese Text | Noto Sans JP fallback 병행 |

### Strategic Rationale

| Reason | Explanation |
|---|---|
| Korean-English compatibility | Pretendard는 한국어와 영어 모두에서 가독성이 높다. |
| Modern SaaS impression | AI·SaaS·디지털 헬스케어 기업에 적합한 현대적 인상을 준다. |
| Clean B2B tone | 일본·싱가포르 전시회용 B2B 자료에 필요한 신뢰감과 정돈된 인상을 제공한다. |
| Brand consistency | 브로슈어, IR, 웹사이트, 제안서의 시각적 일관성을 유지하기 쉽다. |

### Design Rule

> Nursing XR의 공식 전시회·IR·브랜드 자료는 Pretendard를 기본 서체로 사용한다.  
> 일본어 문구가 포함된 자료에서는 Noto Sans JP를 fallback으로 병행하여 가독성을 보완한다.


### Typography Hierarchy

| Role | Font Weight | Size Guide | Usage |
|---|---:|---:|---|
| Hero Title | 700–800 | 44–52px | 표지, IR 커버, 전시회 메인 메시지 |
| Section Heading | 700 | 30–36px | 주요 섹션 제목 |
| Sub-heading | 600–700 | 22–28px | 카드 제목, 소주제 |
| Body | 400–500 | 15–17px | 본문 설명 |
| Caption | 400–500 | 12–14px | 주석, 보조 정보 |
| Badge Text | 600–700 | 11–13px | 키워드 배지, 지표 라벨 |

---

## 6. Layout Principles

Nursing XR 자료는 정보가 많아질 가능성이 높으므로, 디자인의 핵심은 “정돈된 정보 구조”이다.

### Layout Rules

| 원칙 | 설명 |
|---|---|
| White Space First | 과도하게 채우지 않고 여백을 통해 고급스러움과 신뢰감을 만든다. |
| Card-Based Structure | 문제, 솔루션, 기술, 시장, POC를 카드 단위로 분리한다. |
| 3-Column Logic | 1장 소개서와 IR에서는 3분할 구조가 가장 안정적이다. |
| Visual Hierarchy | 가장 중요한 문장은 크게, 세부 설명은 짧게 배치한다. |
| Scannability | 30초 안에 핵심을 파악할 수 있어야 한다. |
| B2B Clarity | 고객, 문제, 해결책, 도입 방식이 명확해야 한다. |

---

## 7. Component Style

### Cards

```css
background: #FFFFFF;
border: 1px solid #DEDEE5;
border-radius: 16px;
box-shadow: rgba(0, 0, 0, 0.03) 0px 4px 24px;
padding: 24px;
```

### Buttons

| Button Type | Style |
|---|---|
| Primary | 보라색 배경 `#7132F5`, 흰 글자, 12px radius |
| Secondary | 흰 배경, 보라색 테두리 `#5741D8`, 보라색 글자 |
| Soft CTA | 연보라 배경 `#F4F0FF`, 보라색 글자 |
| Gray Button | 연회색 배경, 검정 텍스트, 12px radius |

### Badges

| Badge Type | Style |
|---|---|
| Purple Badge | 연보라 배경 + 보라색 텍스트 |
| Green Badge | 연녹색 배경 + 진녹색 텍스트 |
| Neutral Badge | 연회색 배경 + 차콜 텍스트 |
| No Orange Badge | 주황색 배지는 사용하지 않음 |

---

## 8. Brochure Design Principles

일본 전시회와 싱가포르 전시회에서 사용할 브로슈어는 공통 브랜드 체계를 유지하되, 시장별 강조점을 조정한다.

### Master Brochure Structure

| Section | Purpose |
|---|---|
| Cover | Nursing XR의 정체성을 5초 안에 전달 |
| Why Now | 고령화, 의료·돌봄 인력 부족, 실습 교육 한계 제시 |
| Solution | CareXpert와 AI Connect Nurse 구조 설명 |
| Product Experience | 3D Web Simulation, VR Practice, Virtual Patient Interaction |
| Differentiation | 의료교육 전문성, AI 확장성, 시뮬레이션 설계 역량 |
| POC / Partnership | 파일럿, 현지화, 유통, 공동연구 제안 |

---

## 9. IR Deck Design Principles

IR 자료는 기술 설명보다 “고객 중심의 매출형 스토리”가 선행되어야 한다.

### IR Design Rules

| Slide Type | Design Direction |
|---|---|
| Cover | 흰 배경 + 보라색 대형 타이틀 + 핵심 비주얼 |
| Problem | 3개 카드 구조로 시장 문제 제시 |
| Why Japan / Why Singapore | 숫자·시장 키워드·고객 문제 중심 |
| Solution | CareXpert 중심 구조도 |
| Product | 3D Web / VR / AI Connect Nurse 3분할 |
| Differentiation | 기술보다 고객 가치 중심 |
| POC | 3개월 테스트베드 구조를 단계형으로 표현 |
| Business Model | 기관 라이선스, POC, 현지화, B2B/B2G 구조 |
| Ask | 명확한 CTA 박스 |

---

## 10. Product Message Hierarchy

제품 구조는 다음 순서를 유지한다.

```text
Nursing XR
│
├─ CareXpert
│  └─ AI-Powered Healthcare Learning System
│
├─ 3D Web Simulation
│  └─ Accessible scenario-based practice
│
└─ AI Connect Nurse
   └─ Immersive 3D/VR simulation module for nurses and nursing students
```

### Recommended Copy

| Level | English |
|---|---|
| Company | Nursing XR |
| Category | AI-Powered Healthcare Learning System |
| Main Product | CareXpert |
| Nursing Module | AI Connect Nurse |
| Core Capability | 3D Web Simulation + VR Practice + Virtual Patient Interaction |
| Future Direction | AI-driven personalized learning and performance feedback |

---

## 11. Japan Exhibition Design Emphasis

일본 전시회에서는 과장된 기술 이미지보다 신뢰성, 현장성, 실증 가능성을 강조한다.

| 요소 | 방향 |
|---|---|
| Tone | 차분하고 신뢰감 있는 B2B 톤 |
| Key Message | Aging society, workforce readiness, safe repeatable training |
| Visuals | 의료·간호·돌봄 현장 이미지 + 정돈된 시뮬레이션 화면 |
| CTA | Pilot POC, Localization, Institutional Partnership |
| Avoid | 과장된 AI 주장, 게임형 XR 이미지, 네온 과다 사용 |

---

## 12. Singapore Exhibition Design Emphasis

싱가포르 전시회에서는 글로벌 확장성, B2B/B2G 파트너십, 동남아 시장 진출성을 강조한다.

| 요소 | 방향 |
|---|---|
| Tone | 글로벌, 확장성, 비즈니스 중심 |
| Key Message | Scalable healthcare learning system |
| Visuals | AI, 3D/VR, 교육기관·병원·정부 프로그램 연결 |
| CTA | Distribution, B2B/B2G Partnership, Pilot Collaboration |
| Avoid | 간호 VR 콘텐츠만 하는 회사처럼 보이는 표현 |

---

## 13. Image Direction

### Recommended Image Types

| Image Type | Usage |
|---|---|
| Nurse + AI Visual | 표지, 메인 배너 |
| Virtual Patient Interaction | 제품 설명 |
| 3D Simulation Screenshot | 실증 가능성 제시 |
| VR Training Scene | 몰입형 실습 강조 |
| Dashboard / Feedback UI | 향후 AI 학습 시스템 방향 |
| Human Care Image | 돌봄 철학 강조 |

### Avoided Image Types

| Avoided Image | Reason |
|---|---|
| Game-like VR headset only | 단순 VR 체험 기업처럼 보임 |
| Excessive neon metaverse scene | 의료교육 신뢰감 저하 |
| Orange-heavy gradient | 선호하지 않는 색상 |
| Generic hospital stock photo | 차별성 부족 |
| Overly futuristic robot doctor | 인간중심 돌봄 가치 약화 |

---

## 14. Design Quality Checklist

자료 제작 시 아래 기준을 점검한다.

| Checkpoint | Yes / No |
|---|---|
| 보라색이 주조색으로 일관되게 사용되었는가? |  |
| 주황색 계열이 사용되지 않았는가? |  |
| 흰 배경과 충분한 여백이 있는가? |  |
| 의료·교육 분야의 신뢰감이 유지되는가? |  |
| CareXpert와 AI Connect Nurse의 역할이 명확한가? |  |
| 기술보다 고객 문제와 도입 가치가 먼저 보이는가? |  |
| 일본/싱가포르 모두에 확장 가능한 톤인가? |  |
| 30초 안에 핵심 메시지가 이해되는가? |  |
| POC 또는 파트너십 CTA가 명확한가? |  |

---

## 15. Final Design Principle

> Nursing XR의 디자인은 AI 기술의 미래성과 간호·돌봄의 인간적 가치를 동시에 보여주어야 한다.  
> 보라색을 중심으로 전문성과 혁신성을 표현하되, 흰 배경과 정돈된 여백을 통해 의료교육 기업으로서의 신뢰감을 유지한다.  
> 주황색 계열은 사용하지 않으며, 모든 자료는 일본·싱가포르 전시회와 글로벌 IR에서 재사용 가능한 브랜드 시스템으로 설계한다.
