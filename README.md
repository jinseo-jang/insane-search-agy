English | [한국어](README.ko.md)

<div align="center">

# insane-search for Antigravity

**Resilient public page reader & WAF bypass plugin tailored for Google Antigravity 2.0, IDE and CLI**

<p>
  <img src="https://img.shields.io/badge/platform-Antigravity_2.0-4285F4?logo=googlecloud&style=flat-square" alt="Antigravity 2.0">
</p>

This repository is a dedicated port of [fivetaku/insane-search](https://github.com/fivetaku/insane-search) optimized for Google Antigravity 2.0, IDE and CLI environments.  
For general engine architecture and platform specifications, refer to the [upstream repository](https://github.com/fivetaku/insane-search).

</div>

---

## Antigravity Installation Guide

### Step 1: Clone Git Repository
```bash
git clone https://github.com/jinseo-jang/insane-search-agy.git
cd insane-search-agy
```

### Step 2: Copy Skill Directory

#### A. Global Skill Installation (Recommended)
Available across all Google Antigravity 2.0, IDE and CLI sessions:
```bash
mkdir -p ~/.gemini/config/skills
cp -r skills/insane-search ~/.gemini/config/skills/
```

#### B. Project Local Skill Installation
Scoped exclusively to the current project workspace:
```bash
mkdir -p .agents/skills
cp -r skills/insane-search .agents/skills/
```

---

## Usage

Request via plain natural language or execute directly using slash commands or CLI modules.

### 1. Natural Language Prompts
- "Scrape Coupang for laptop deals under $1000"
- "Find what people are saying about Antigravity on Reddit and summarize top threads"
- "Fetch recent commits from GitHub repository fivetaku/insane-search"
**Natural Prompt Triggers:** twitter access, reddit blocked, youtube subtitles, github search, arxiv papers, threads, mastodon, medium, substack, stackoverflow, naver blog, dcinside, fmkorea, coupang, linkedin, yozm, wishket

### 2. Slash Command & Direct CLI Execution
```bash
/insane-search <URL>

# Direct CLI module execution:
cd skills/insane-search && python3 -m engine "<URL>"

# Or using PYTHONPATH:
PYTHONPATH=skills/insane-search python3 -m engine "<URL>"
```

---

## Key Differences: Upstream vs. Antigravity Port

| Feature | Upstream Original (`fivetaku/insane-search`) | Antigravity Port (`insane-search-agy`) |
| :--- | :--- | :--- |
| **Target Agent** | Claude Code CLI / Plugin Ecosystem | **Google Antigravity 2.0, IDE and CLI** |
| **Skill Location** | Claude Plugin Registry (`claude plugin add`) | `~/.gemini/config/skills/` and `.agents/skills/` |
| **Dependencies & Fallbacks** | Manual user pre-installation | **Cross-Platform Auto-Discovery & Rule R6**: Engine-level Node discovery (e.g. `/opt/homebrew/bin/node`) across macOS, Linux, and Windows plus Rule R6 exhaustive attempt enforcement, with Patchright auto-setup (`npx patchright install chrome`) |
| **Safety Isolation** | Standard plain text return | **Rule R8 Enforced**: `[BEGIN UNTRUSTED WEB CONTENT]` boundary tags |

---

## License

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.  
Original work Copyright (c) 2026 fivetaku. Antigravity Port Copyright (c) 2026 Jinseo Jang.
