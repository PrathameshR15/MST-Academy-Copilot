(function() {
    // Inject CSS
    const currentScript = document.currentScript;
    const scriptUrl = currentScript ? currentScript.src : window.location.href;
    const baseUrl = scriptUrl.substring(0, scriptUrl.lastIndexOf('/'));
    const apiUrl = baseUrl.replace('/static', '/api');

    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `${baseUrl}/widget.css`;
    document.head.appendChild(link);

    // Inject Marked.js for Markdown parsing
    const markedScript = document.createElement('script');
    markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    document.head.appendChild(markedScript);

    // Create Widget Container
    const container = document.createElement('div');
    container.id = 'mst-chat-widget-container';
    document.body.appendChild(container);

    // HTML Structure
    container.innerHTML = `
        <div id="mst-chat-widget-window">
            <div id="mst-chat-widget-header">
                <div style="display: flex; align-items: center;">
                    <div class="mst-chat-widget-robot-mascot">🤖</div>
                    <div class="mst-chat-widget-title">
                        <span>MST Academy</span>
                        <span class="mst-chat-widget-subtitle">Support Assistant</span>
                    </div>
                </div>
                <button id="mst-chat-widget-close">&times;</button>
            </div>
            <div id="mst-chat-widget-messages">
                <div class="mst-chat-widget-message mst-chat-widget-assistant">
                    Hello! How can I help you with Academy support?
                </div>
            </div>
            <div id="mst-chat-widget-input-area">
                <input type="text" id="mst-chat-widget-input" placeholder="Ask your question..." autocomplete="off"/>
                <button id="mst-chat-widget-send" disabled>
                    <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                </button>
            </div>
        </div>
        <button id="mst-chat-widget-button">
            <!-- Robot SVG -->
            <svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 0 1 2 2v2h3a2 2 0 0 1 2 2v2h2v4h-2v2a2 2 0 0 1-2 2h-3v2a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2v-2H5a2 2 0 0 1-2-2v-2H1v-4h2V8a2 2 0 0 1 2-2h3V4a2 2 0 0 1 2-2h2zM5 10v6h14v-6H5zm3 2h2v2H8v-2zm6 0h2v2h-2v-2z"/></svg>
        </button>
    `;

    // DOM Elements
    const chatWindow = document.getElementById('mst-chat-widget-window');
    const chatButton = document.getElementById('mst-chat-widget-button');
    const closeBtn = document.getElementById('mst-chat-widget-close');
    const messagesArea = document.getElementById('mst-chat-widget-messages');
    const inputField = document.getElementById('mst-chat-widget-input');
    const sendBtn = document.getElementById('mst-chat-widget-send');

    let history = [];
    let isWaiting = false;

    // Toggle Window
    function toggleWindow() {
        chatWindow.classList.toggle('mst-chat-widget-open');
        chatButton.classList.toggle('mst-chat-widget-hidden');
        if (chatWindow.classList.contains('mst-chat-widget-open')) {
            inputField.focus();
        }
    }

    chatButton.addEventListener('click', toggleWindow);
    closeBtn.addEventListener('click', toggleWindow);

    // Input state
    inputField.addEventListener('input', () => {
        sendBtn.disabled = inputField.value.trim() === '' || isWaiting;
    });

    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !sendBtn.disabled) {
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', () => {
        if (!sendBtn.disabled) {
            sendMessage();
        }
    });

    // Helper: Scroll to bottom
    function scrollToBottom() {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    // Send Message
    async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        // Add user message to UI
        appendMessage('user', text);
        
        // Update history
        const currentHistory = [...history]; // copy for payload
        history.push({ role: 'user', text: text });

        inputField.value = '';
        inputField.disabled = true;
        sendBtn.disabled = true;
        isWaiting = true;

        // Show loading indicator
        const loadingId = 'mst-chat-loading-' + Date.now();
        messagesArea.innerHTML += `<div id="${loadingId}" class="mst-chat-widget-loading"><span></span><span></span><span></span></div>`;
        scrollToBottom();

        try {
            const response = await fetch(`${apiUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    history: currentHistory,
                    provider: 'openai'
                })
            });

            const data = await response.json();
            
            // Remove loading
            document.getElementById(loadingId)?.remove();

            if (response.ok) {
                appendMessage('assistant', data.answer, data.source);
                history.push({ role: 'assistant', text: data.answer });
            } else {
                appendMessage('assistant', "I'm having trouble connecting to the server. Please try again.");
            }

        } catch (err) {
            document.getElementById(loadingId)?.remove();
            appendMessage('assistant', "An error occurred while sending your message. Please try again.");
        } finally {
            inputField.disabled = false;
            isWaiting = false;
            inputField.focus();
            scrollToBottom();
        }
    }

    // Append Message to UI
    function appendMessage(role, text, source = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `mst-chat-widget-message mst-chat-widget-${role}`;
        
        if (role === 'assistant' && typeof marked !== 'undefined') {
            msgDiv.innerHTML = marked.parse(text);
        } else {
            msgDiv.textContent = text;
        }

        messagesArea.appendChild(msgDiv);

        // Add source badge if applicable
        if (source && source !== "NONE") {
            let sourceText = "Information not found";
            if (source === 'LOCAL_KB') sourceText = "Source: Academy Knowledge Base";
            else if (source === 'WEBSITE') sourceText = "Source: MST Academy Website";
            else if (source === 'BOTH') sourceText = "Source: Academy Knowledge Base + Website";
            
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'mst-chat-widget-source';
            sourceDiv.textContent = sourceText;
            messagesArea.appendChild(sourceDiv);
        }

        scrollToBottom();
    }
})();
