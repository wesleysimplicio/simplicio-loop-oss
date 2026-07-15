# simplicio-loop-oss

<p align="center"><img src="../output/imagegen/simplicio-loop-oss-hero.png" alt="حلقة مستمرة للمساهمة في المصادر المفتوحة حول مستودع" width="100%"></p>

<p align="center"><strong>حلقة دائمة محكومة بالجودة للمساهمة في مستودعات المصادر المفتوحة.</strong><br>يصبح الاستطلاع سياقاً، ويصبح السياق طلب سحب صغيراً ومختبراً. كل دورة تجعل استئناف العمل أسهل.</p>

<p align="center"><a href="../README.md">English</a> · <a href="README.pt-BR.md">Português</a> · <a href="README.es-ES.md">Español</a> · <a href="README.ja-JP.md">日本語</a> · <a href="README.ko-KR.md">한국어</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.it-IT.md">Italiano</a> · <a href="README.fr-FR.md">Français</a> · <a href="README.ru-RU.md">Русский</a> · <a href="README.pl-PL.md">Polski</a> · <a href="README.hi-IN.md">हिन्दी</a> · <a href="README.ar-SA.md">العربية</a> · <a href="README.he-IL.md">עברית</a> · <a href="README.ms-MY.md">Bahasa Melayu</a> · <a href="README.id-ID.md">Bahasa Indonesia</a></p>

<p align="center"><img src="../output/imagegen/simplicio-loop-oss-mission-control.png" alt="حلقة مستمرة للمساهمة في المصادر المفتوحة حول مستودع" width="100%"></p>

## لماذا يوجد المشروع

يصبح الاستطلاع سياقاً، ويصبح السياق طلب سحب صغيراً ومختبراً. كل دورة تجعل استئناف العمل أسهل.

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

المتطلبات: git وPython 3.10+ وgh موثّق ومضيف LLM قادر على تنفيذ أوامر shell.

~~~text
Run the simplicio-loop-oss skill for one iteration against owner/repo
~~~

راجع الدليل الكامل في README بالإنجليزية.

## Persistent state

يحتوي projects/<owner>__<repo>/ على PROFILE.md والسجلات وbacklog والتدقيق وopened-prs.md. الحالة المصدّرة وسيلة التسليم بين الأجهزة والوكلاء.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wesleysimplicio/simplicio-loop-oss&type=Date)](https://star-history.com/#wesleysimplicio/simplicio-loop-oss&Date)

