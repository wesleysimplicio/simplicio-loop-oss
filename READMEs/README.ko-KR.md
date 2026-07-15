# simplicio-loop-oss

<p align="center"><img src="../output/imagegen/simplicio-loop-oss-hero.png" alt="저장소를 둘러싼 지속적인 오픈소스 기여 루프" width="100%"></p>

<p align="center"><strong>오픈소스 저장소를 위한 영속적이고 품질 게이트가 있는 기여 루프입니다.</strong><br>정찰은 컨텍스트가 되고, 컨텍스트는 작고 테스트된 풀 리퀘스트가 됩니다. 각 반복은 다음 작업을 쉽게 재개하도록 합니다.</p>

<p align="center"><a href="../README.md">English</a> · <a href="README.pt-BR.md">Português</a> · <a href="README.es-ES.md">Español</a> · <a href="README.ja-JP.md">日本語</a> · <a href="README.ko-KR.md">한국어</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.it-IT.md">Italiano</a> · <a href="README.fr-FR.md">Français</a> · <a href="README.ru-RU.md">Русский</a> · <a href="README.pl-PL.md">Polski</a> · <a href="README.hi-IN.md">हिन्दी</a> · <a href="README.ar-SA.md">العربية</a> · <a href="README.he-IL.md">עברית</a> · <a href="README.ms-MY.md">Bahasa Melayu</a> · <a href="README.id-ID.md">Bahasa Indonesia</a></p>

<p align="center"><img src="../output/imagegen/simplicio-loop-oss-mission-control.png" alt="저장소를 둘러싼 지속적인 오픈소스 기여 루프" width="100%"></p>

## 왜 필요한가

정찰은 컨텍스트가 되고, 컨텍스트는 작고 테스트된 풀 리퀘스트가 됩니다. 각 반복은 다음 작업을 쉽게 재개하도록 합니다.

- Study the repository before changing code.
- Keep backlog, issues, and pull requests free of duplicates.
- Prefer small, tested changes that can merge.
- Persist profiles, logs, audits, and history so work can resume on any machine.

## How it works

~~~mermaid
flowchart LR
    subgraph CONTEXT["CONTEXT"]
        A["owner/repo"] --> B["Bootstrap and sync"]
        B --> C["Phase R reconnaissance"]
        C --> D["Committed PROFILE.md"]
    end
    subgraph EXECUTION["EXECUTION"]
        D --> E["Rank backlog"]
        E --> F["Deduplicate twice"]
        F --> G["Focused change"]
        G --> H["Fail-before / pass-after tests"]
        H --> I["Adversarial review"]
    end
    subgraph PROOF["PROOF"]
        I --> J["Open or update PR"]
        J --> K["Commit logs and audit state"]
        K --> L["Merge-rate feedback"]
        L -. "next iteration" .-> E
    end
~~~

## Quick start

필요한 것: git, Python 3.10 이상, 인증된 gh, 셸 명령을 실행할 수 있는 LLM 호스트.

~~~text
Run the simplicio-loop-oss skill for one iteration against owner/repo
~~~

전체 가이드는 영문 README에서 확인하세요.

## Persistent state

projects/<owner>__<repo>/ 에 PROFILE.md, 로그, backlog, 감사 결과와 opened-prs.md를 저장합니다.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wesleysimplicio/simplicio-loop-oss&type=Date)](https://star-history.com/#wesleysimplicio/simplicio-loop-oss&Date)

