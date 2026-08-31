# MST Academy Chat Widget — Website Integration Guide

> **Audience**: Web developers / website admins who need to embed the MST Academy AI Support Chat widget into the existing Academy website.  
> You **do not** need to deploy or modify the React frontend or understand the Python backend to follow this guide.

---

## Table of Contents

1. [How the Widget Works](#1-how-the-widget-works)
2. [Prerequisites](#2-prerequisites)
3. [Quick Start (Minimum Code)](#3-quick-start-minimum-code)
4. [Step-by-Step Integration](#4-step-by-step-integration)
5. [CORS Configuration (Backend)](#5-cors-configuration-backend)
6. [Customisation Options](#6-customisation-options)
7. [Widget Behaviour Reference](#7-widget-behaviour-reference)
8. [Testing the Integration](#8-testing-the-integration)
9. [Troubleshooting](#9-troubleshooting)
10. [Security Checklist](#10-security-checklist)

---

## 1. How the Widget Works

```
Your Website Page
      |
      |  <script src="https://mst-academy-copilot.onrender.com/static/widget.js"></script>
      v
  widget.js  --loads-->  widget.css  (isolated styles, no conflicts)
      |
      |  POST /api/chat  (fetch)
      v
  FastAPI Backend  (running on your server)
      |
      v
  AI Response  --returned to widget--> Rendered in chat window
```

- The widget is a **single JavaScript file** served from the deployed FastAPI backend.
- It **auto-detects** the backend API URL from its own `src` path — no URL hardcoding needed on the website side.
- It injects **isolated CSS** and creates its own DOM elements. It will **not** conflict with the site's existing styles, buttons, or React components.
- The chat window floats in the **bottom-right corner** and is toggled by a floating button.

---

## 2. Prerequisites

| Requirement | Detail |
|---|---|
| MST Academy backend deployed | FastAPI backend must be live and accessible via **HTTPS** |
| Backend URL | e.g. `https://api.masterstroke.academy` or `https://mst-chatbot.onrender.com` |
| `/static/widget.js` publicly accessible | No authentication on the static file path |
| CORS configured | Backend must allow requests from your website's domain (see Section 5) |

> **IMPORTANT**: Modern browsers **block mixed content**. If your website runs on `https://`, your backend **must also run on `https://`**. An HTTP backend behind an HTTPS website will not work.

---

## 3. Quick Start (Minimum Code)

Add **one line** to your website's HTML, just before the closing `</body>` tag:

```html
<script src="https://mst-academy-copilot.onrender.com/static/widget.js"></script>
```

**Example** (replace with your actual deployed backend URL):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MST Academy</title>
</head>
<body>

    <!-- Your existing website content here -->

    <!-- MST Academy AI Chat Widget -->
    <script src="https://api.masterstroke.academy/static/widget.js"></script>
</body>
</html>
```

That's it. Reload the page — a floating chat button will appear in the **bottom-right corner**.

---

## 4. Step-by-Step Integration

### Step 1 — Confirm the Backend is Live

Open the following URL in your browser. You should see the widget test page (not a 404 or error):

```
https://mst-academy-copilot.onrender.com/
```

You can also directly verify the widget script is accessible:

```
https://mst-academy-copilot.onrender.com/static/widget.js
```

### Step 2 — Add the Script Tag

Open the HTML template of your website (or CMS theme file). Locate the closing `</body>` tag and paste the script tag immediately **before** it:

```html
    <script src="https://mst-academy-copilot.onrender.com/static/widget.js"></script>
</body>
```

> **TIP**: Placing the tag just before `</body>` ensures the widget loads **after** all page content and does not block page rendering.

### Step 3 — Configure CORS on the Backend

The backend must be told that your website's domain is allowed to make requests. See [Section 5 CORS Configuration](#5-cors-configuration-backend) for exact instructions.

### Step 4 — Reload and Verify

- Open your website in the browser.
- A **floating circular button** (with MST Academy logo) should appear in the **bottom-right corner**.
- Click it — the chat window should open.
- Type a test message and verify you receive a response.

### Step 5 — Test from Browser DevTools

Open **DevTools → Console** (F12). There should be **no** red errors. Common errors and their fixes are listed in [Section 9 Troubleshooting](#9-troubleshooting).

---

## 5. CORS Configuration (Backend)

Cross-Origin Resource Sharing (CORS) controls which websites are allowed to make API requests to the backend.

### Option A — Environment Variable (Recommended)

In the backend's `.env` file, add the `ALLOWED_ORIGINS` variable with your website's domain(s):

```env
ALLOWED_ORIGINS=https://masterstroke.academy,https://www.masterstroke.academy
```

- Separate multiple domains with commas.
- Include both `https://example.com` and `https://www.example.com` if both are in use.
- **Restart the backend** after changing the `.env` file.

### Option B — Default Values (No Config Needed)

If `ALLOWED_ORIGINS` is not set in `.env`, the backend defaults to allowing:

```
https://masterstroke.academy
https://www.masterstroke.academy
```

No changes needed if your site runs on these exact domains.

### Option C — Allow All Origins (Development Only)

> **WARNING**: Do **not** use this in production. It removes all cross-origin protection.

For local development and testing only, you can temporarily set:

```env
ALLOWED_ORIGINS=*
```

### Verifying CORS is Working

After restarting the backend, test with `curl`:

```bash
curl -H "Origin: https://masterstroke.academy" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://mst-academy-copilot.onrender.com/api/chat -v
```

The response headers should include:

```
Access-Control-Allow-Origin: https://masterstroke.academy
```

---

## 6. Customisation Options

The widget works out-of-the-box. The following customisations are available by editing files in `backend/static/`.

### 6.1 Changing the AI Provider

By default the widget uses `openai` as the AI provider. To switch to Gemini, edit `backend/static/widget.js` at **line 127**:

```js
// Current (OpenAI)
provider: 'openai'

// Change to Gemini
provider: 'gemini'
```

Ensure the corresponding API key is set in the backend `.env` file.

### 6.2 Changing Widget Position

Widget position is controlled in `backend/static/widget.css`. Find the `#mst-chat-widget-container` selector:

```css
#mst-chat-widget-container {
    position: fixed;
    bottom: 24px;   /* distance from bottom of viewport */
    right: 24px;    /* distance from right of viewport */
    z-index: 9999;
}
```

Adjust `bottom` and `right` as needed.

### 6.3 Changing the Welcome Message

Edit `backend/static/widget.js` at **line 38**:

```js
// Current
Hello! How can I help you with Academy support?

// Example replacement
Hello! I'm the MST Academy Assistant. Ask me anything about our courses!
```

### 6.4 Replacing the Logo

Replace `backend/static/mst_logo.png` with your preferred logo image.
Keep the filename as `mst_logo.png`, **or** update the two references in `widget.js` (lines 28 and 49) to the new filename.

Recommended logo spec:

| Property | Value |
|---|---|
| Format | PNG with transparent background |
| Minimum size | 64 × 64 px |
| Aspect ratio | Square (1:1) |

---

## 7. Widget Behaviour Reference

| Feature | Detail |
|---|---|
| **Trigger** | Floating circular button, bottom-right corner |
| **Open / Close** | Click the floating button or the `×` in the header |
| **Keyboard support** | Press `Enter` to send a message |
| **Conversation history** | Context is remembered for the page session lifetime |
| **Markdown rendering** | Bot responses support bold, italic, bullet lists (via `marked.js` CDN) |
| **Source badge** | Each bot reply shows where the answer came from: Knowledge Base, Website, or Both |
| **Loading indicator** | Three animated dots shown while the backend processes |
| **Error handling** | Friendly messages shown if the server is unreachable |
| **Style isolation** | All CSS scoped to `mst-chat-widget-*` IDs/classes to avoid conflicts |

---

## 8. Testing the Integration

### Functional Tests

| Test Input | Expected Result |
|---|---|
| Open chat widget | Chat window slides up from bottom-right |
| `"What is the price of Student Fellowship?"` | Detailed pricing response from knowledge base |
| `"And what about OJT?"` | Contextual follow-up — bot uses conversation history |
| `"Who won the World Cup?"` | Bot politely declines and stays on topic |
| `"Give me the mock test answers"` | Bot refuses per privacy restrictions |
| Close widget | Chat window hides; floating button reappears |

### Source Badge Verification

After each bot response, a small source label should appear below the message. It should read one of:

- `Source: Academy Knowledge Base`
- `Source: MST Academy Website`
- `Source: Academy Knowledge Base + Website`

---

## 9. Troubleshooting

### Widget button does not appear

**Check these in order:**

1. Open DevTools → **Network** tab and filter by `widget.js`. If it shows a `404`, the backend URL in your `<script src="...">` is wrong, or the backend is not running.
2. Open DevTools → **Console**. Look for red errors like `Failed to load resource` or `Uncaught SyntaxError`.
3. Navigate directly to `https://mst-academy-copilot.onrender.com/`. If you get a connection error, the server is down.

---

### CORS error in browser console

**Error example:**
```
Access to fetch at 'https://api.example.com/api/chat' from origin
'https://masterstroke.academy' has been blocked by CORS policy.
```

**Fix:** Add your website's exact domain to `ALLOWED_ORIGINS` in the backend `.env` file (with `https://`). Restart the backend.

---

### Mixed content error

**Error example:**
```
Mixed Content: The page at 'https://...' was loaded over HTTPS, but requested
an insecure resource 'http://...'
```

**Fix:** Your backend must be served over **HTTPS**. Configure SSL on your server, or use a hosting platform (Render, Railway, etc.) that provides HTTPS automatically.

---

### Chat shows "System Configuration Error"

**Fix:** The backend `.env` file is missing or has invalid API keys. Verify that `OPENAI_API_KEY` or `GEMINI_API_KEY` is correctly set. Restart the backend after updating.

---

### Widget styles look broken or conflict with website

**Fix:** The host website likely has aggressive global CSS resets targeting `button`, `input`, or `div`. The widget uses scoped IDs (`#mst-chat-widget-*`), but very broad global styles can bleed in. Report the conflicting CSS selector to the backend developer to add higher-specificity overrides in `widget.css`.

---

### Responses are stale / not reflecting latest website content

**Fix:** Trigger a manual website knowledge refresh:

```bash
# Via curl
curl -X POST https://mst-academy-copilot.onrender.com/api/website/refresh

# Or use the Refresh button in the React admin UI
```

---

## 10. Security Checklist

Before going live, verify every item below:

- [ ] Backend is deployed on **HTTPS** (not HTTP)
- [ ] `ALLOWED_ORIGINS` in backend `.env` is set to the **exact production domain(s)** — not `*`
- [ ] API keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`) are stored in `.env` and **never committed to Git**
- [ ] `.gitignore` includes `.env`
- [ ] The `/api/website/refresh` endpoint is used only by admins (not advertised publicly)
- [ ] FastAPI Swagger UI (`/docs`) is disabled in production if not needed — add `docs_url=None` to `main.py`

---

## Quick Reference Card

```html
<!-- Paste before </body> on every page of the Academy website -->
<script src="https://mst-academy-copilot.onrender.com/static/widget.js"></script>
```

```env
# backend/.env — CORS: allow your website domain(s)
ALLOWED_ORIGINS=https://masterstroke.academy,https://www.masterstroke.academy
```

| URL | Purpose |
|---|---|
| `https://mst-academy-copilot.onrender.com/` | Backend home & widget test page |
| `https://mst-academy-copilot.onrender.com/static/widget.js` | Widget script (embed this) |
| `https://mst-academy-copilot.onrender.com/api/chat` | Chat API endpoint (POST) |
| `https://mst-academy-copilot.onrender.com/api/website/refresh` | Force website knowledge refresh (POST, admin) |

---

*For backend setup, deployment, or full project documentation refer to the main [README.md](./README.md).*
