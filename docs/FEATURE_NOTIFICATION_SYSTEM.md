# Feature: Knowledge Delivery & Notification System

**Status**: SUPERSEDED — historical reference only.
**Previous implementation**: `archive/notifications-v1/`

> ⚠️ **Stale as of 2026-03-29**: the n8n webhook layer described below was removed. The
> `n8n.vecia.fr/webhook/video-processed` endpoint no longer exists. Telegram delivery is
> now handled by the Hermes gateway on gaming-PC, not n8n or a standalone notifier. Read
> this only for the v1 formatter design (AI-Tools / Sports); ignore the n8n integration
> points. Delivery reminders (spaced repetition, weekly digest) are Phase 2/3 roadmap work,
> not yet built.

## What Worked (v1)

### Immediate Rich Notifications
- Telegram HTML-formatted messages after video processing
- Domain-specific formatters:
  - **AI Tools**: Title, summary, top 5 takeaways, tools mentioned, key insights
  - **Sports**: Evidence tier, protocols, biomechanical notes
- Triggered via Python CLI or n8n webhook

### Integration Points
- Python CLI: `uv run python notifications/scripts/send_notification.py <analysis.json>`
- n8n webhook: POST to `https://n8n.vecia.fr/webhook/video-processed`
- Direct Python API: `TelegramNotifier` + `AIToolsFormatter`/`SportsFormatter`

### Architecture
- `src/core/telegram_client.py` — Telegram Bot API client
- `src/core/webhook_notifier.py` — FastAPI webhook handler (deployed on gaming-PC)
- `src/formatters/` — Domain-specific message formatters
- `config/config.yaml` — Bot token + chat ID (secret, never committed)

## Planned but Not Implemented

### Weekly Synthesis Digest
- Cross-cutting themes across videos processed that week
- Sunday evening delivery
- Patterns and connections humans miss when watching individually

### Spaced Repetition
- Daily delivery of insights from 1 week, 1 month, 3 months ago
- Scientifically-proven retention technique applied to video knowledge
- Configurable delivery time

### Multi-Channel Delivery
- Email digest support
- Notion page creation
- Slack/Discord integration
- Voice message summaries (Telegram voice notes)

## BMAD Discussion Needed

The notification system is one piece of a broader **intake/dispatch/notification architecture**:

1. **Intake Channels**: WhatsApp URL sharing, Notion Video Inbox, direct CLI, API endpoint
2. **Dispatch**: How URLs get routed to the correct pipeline (AI tools vs Sports vs Vimeo)
3. **Processing**: The existing dual pipeline (extract → enhance → analyze → store)
4. **Notification**: Post-processing delivery of insights to the user
5. **Retention**: Spaced repetition and weekly synthesis for long-term learning

Each of these deserves proper BMAD treatment to design the right architecture before rebuilding. The v1 notification code in `archive/notifications-v1/` provides a solid reference for the Telegram integration pattern.
