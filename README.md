# Smart Twitter Reply Bot

AI agent that intelligently replies to mentions on X.  
Supports **Grok**, **OpenAI**, or **Claude** (choose via `LLM_PROVIDER`).

[![Grok-Installed](https://img.shields.io/badge/Grok-Installed-00f0ff?style=for-the-badge&logo=x&logoColor=white)](https://x.com/i/grok?grok-install=true)

## Features (v2.2)
- Multi-LLM support: Grok, OpenAI GPT, or Claude
- One-click install via grok-install
- Automatic replies to mentions
- Passive Growth Engine enabled (auto-welcome on X)
- Shareable install card

## Quick Install
1. Click the blue "Install with Grok" button (or post this repo link on X)
2. Choose your preferred LLM (grok / openai / claude)
3. Provide the required API keys when asked by Grok
4. Deploy (defaults to Railway)

## Configuration
See `grok-install.yaml` for all options.

## Environment Variables (see .env.example)
- `LLM_PROVIDER` → grok | openai | claude
- API keys for the chosen LLM + X credentials

Built with ❤️ using grok-install v2.2  
Multi-LLM ready • Phase 6 compatible

Made live with @JanSol0s (Jani) & Grok.
