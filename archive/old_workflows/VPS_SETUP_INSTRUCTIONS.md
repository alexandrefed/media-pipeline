# VPS Setup Instructions
## AI Knowledge Base n8n Integration

**Give these instructions to VPS Claude Code**

---

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
cd /opt/vecia
git clone <REPO_URL> AI-Knowledge-Base-PRD
cd AI-Knowledge-Base-PRD
```

**Replace `<REPO_URL>` with the actual GitHub repository URL**

---

### Step 2: Install Python Dependencies

```bash
cd notifications
python3 -m pip install -r requirements.txt
```

**Expected packages:**
- requests
- pyyaml
- psycopg2-binary (for database access)

---

### Step 3: Configure Telegram Bot

```bash
cd config
cp config.example.yaml config.yaml
nano config.yaml
```

**Update these values:**
```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
  chat_id: "YOUR_CHAT_ID_HERE"       # Your Telegram chat ID
```

**To get your chat ID:**
1. Message your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{"id":123456789}`

---

### Step 4: Test Notification Script

```bash
cd /opt/vecia/AI-Knowledge-Base-PRD/notifications
python3 scripts/send_notification.py \
  --title "VPS Test" \
  --message "Notification system working on VPS!" \
  --priority high
```

**Expected result:** Telegram message received in your chat

**If error occurs:**
- Check bot token is correct
- Check chat ID is correct
- Verify dependencies installed: `pip3 list | grep -E "requests|pyyaml"`

---

### Step 5: Update Docker Compose

```bash
cd /opt/vecia
nano docker-compose.yml
```

**Find the `vecia_n8n` service and update volumes section:**

```yaml
vecia_n8n:
  image: n8nio/n8n:latest
  container_name: vecia_n8n
  restart: unless-stopped
  ports:
    - "5678:5678"
  environment:
    - N8N_HOST=n8n.vecia.fr
    - WEBHOOK_URL=https://n8n.vecia.fr/
    - GENERIC_TIMEZONE=Europe/Paris
  volumes:
    - n8n_data:/home/node/.n8n
    # ADD THIS SECTION:
    - type: bind
      source: /opt/vecia/AI-Knowledge-Base-PRD/notifications
      target: /notifications
      read_only: true
  networks:
    - vecia_network
```

**Key points:**
- ✅ Use `type: bind` (not `-` syntax)
- ✅ `source:` is the FULL path on VPS
- ✅ `target:` is `/notifications` (fixed)
- ✅ `read_only: true` is CRITICAL for security

---

### Step 6: Restart n8n Container

```bash
docker-compose restart vecia_n8n
```

**Expected output:**
```
Restarting vecia_n8n ... done
```

**Check logs:**
```bash
docker-compose logs -f vecia_n8n
```
Look for successful restart, no errors

---

### Step 7: Verify Mount Inside Container

```bash
# Check directory exists
docker exec vecia_n8n ls -la /notifications

# Check Python is available
docker exec vecia_n8n python3 --version

# Check script is accessible
docker exec vecia_n8n python3 /notifications/scripts/send_notification.py --help
```

**Expected outputs:**
1. Directory listing showing `config/`, `scripts/`, `src/`
2. Python version (should be 3.x)
3. Script help message

---

### Step 8: Test from Inside Container

```bash
docker exec vecia_n8n python3 /notifications/scripts/send_notification.py \
  --title "Container Test" \
  --message "Can execute from inside n8n container!" \
  --priority high
```

**Expected result:** Telegram message received

**This confirms:**
- ✅ Bind mount working
- ✅ Python available in container
- ✅ Scripts executable from n8n
- ✅ Telegram API accessible

---

### Step 9: Verify Database Connection (Optional)

```bash
# Test PostgreSQL connection from host
docker exec vecia_aidb psql -U ai_admin -d aidb -c "SELECT * FROM ai_kb.kb_videos LIMIT 1;"
```

**Expected:** No error (even if empty result)

---

## Troubleshooting

### Issue: "Permission denied" when accessing /notifications

**Solution:**
```bash
# Check ownership
ls -la /opt/vecia/AI-Knowledge-Base-PRD/notifications

# If needed, fix permissions
sudo chown -R $USER:$USER /opt/vecia/AI-Knowledge-Base-PRD
chmod -R 755 /opt/vecia/AI-Knowledge-Base-PRD
```

---

### Issue: "Module not found: requests"

**Solution:**
```bash
# Install in container (temporary - won't persist)
docker exec vecia_n8n pip install requests pyyaml

# OR install on host (better)
cd /opt/vecia/AI-Knowledge-Base-PRD/notifications
python3 -m pip install --user -r requirements.txt
```

---

### Issue: Telegram bot not responding

**Check:**
1. Bot token is correct in `config.yaml`
2. Chat ID is correct (numeric, not username)
3. Bot is not blocked
4. Internet access from container works: `docker exec vecia_n8n ping -c 3 api.telegram.org`

---

### Issue: Scripts work on host but not in container

**Check Python path:**
```bash
# Inside container
docker exec vecia_n8n which python3
docker exec vecia_n8n python3 -c "import sys; print(sys.path)"

# Check if packages installed
docker exec vecia_n8n pip3 list
```

---

## Success Checklist

After completing all steps, verify:

- [ ] Repository cloned to `/opt/vecia/AI-Knowledge-Base-PRD`
- [ ] Python dependencies installed
- [ ] Telegram bot token configured in `config/config.yaml`
- [ ] Test notification sent from VPS successfully
- [ ] Docker compose updated with bind mount
- [ ] n8n container restarted without errors
- [ ] Bind mount visible inside container (`docker exec vecia_n8n ls /notifications`)
- [ ] Python script executable from container
- [ ] Test notification sent FROM container successfully
- [ ] Database connection working (optional)

---

## Report Back

**Once complete, report:**

```
✅ VPS Setup Complete

Repository: /opt/vecia/AI-Knowledge-Base-PRD
Python: <version>
Telegram: <bot name> → <your chat>
Mount: /notifications (read-only)
Test: Notification sent successfully from container

Ready for workflow updates!
```

---

## Next Steps (Mac Claude Code will handle)

After you report completion:
1. Mac Claude will update n8n workflow paths
2. Mac Claude will test webhooks
3. Mac Claude will export workflow backups
4. System will be ready for production use

---

**Need help?** Paste any error messages and I'll help troubleshoot.
