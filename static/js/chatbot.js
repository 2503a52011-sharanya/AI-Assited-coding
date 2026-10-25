// AI Travel Chatbot Interface
document.addEventListener('DOMContentLoaded', () => {
    const chatBubble = document.getElementById('chatBubble');
    const chatWindow = document.getElementById('chatWindow');
    const chatClose = document.getElementById('chatClose');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const quickPrompts = document.querySelectorAll('.chat-quick-prompt');

    if (!chatBubble || !chatWindow) return;

    let sessionId = localStorage.getItem('smart_travel_chat_session') || null;

    // Toggle Chat Window
    chatBubble.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        if (!chatWindow.classList.contains('hidden')) {
            chatInput.focus();
            scrollToBottom();
        }
    });

    chatClose.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
    });

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function formatMarkdown(text) {
        // Simple markdown formatter for links, bold, bullets
        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-teal-600 underline font-semibold hover:text-teal-800">$1</a>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n• /g, '<br>• ');
        return formatted;
    }

    function appendMessage(sender, content) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-3`;

        const bubble = document.createElement('div');
        bubble.className = `max-w-[85%] rounded-2xl px-4 py-2.5 text-sm shadow-sm ${
            sender === 'user'
                ? 'bg-gradient-to-r from-teal-600 to-emerald-600 text-white rounded-br-none'
                : 'bg-white border border-gray-100 text-gray-800 rounded-bl-none'
        }`;
        
        if (sender === 'user') {
            bubble.textContent = content;
        } else {
            bubble.innerHTML = formatMarkdown(content);
        }

        msgDiv.appendChild(bubble);
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'flex justify-start mb-3';
        typingDiv.innerHTML = `
            <div class="bg-gray-100 text-gray-400 rounded-2xl rounded-bl-none px-4 py-2 text-xs flex items-center space-x-1">
                <span class="animate-bounce">●</span>
                <span class="animate-bounce" style="animation-delay: 0.2s">●</span>
                <span class="animate-bounce" style="animation-delay: 0.4s">●</span>
                <span class="ml-2 font-medium">Gemini AI is analyzing travel routes...</span>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const ind = document.getElementById('typingIndicator');
        if (ind) ind.remove();
    }

    async function sendMessage(text) {
        const clean = text.trim();
        if (!clean) return;

        appendMessage('user', clean);
        if (chatInput) chatInput.value = '';
        appendTypingIndicator();

        try {
            const res = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: clean,
                    session_id: sessionId
                })
            });

            const data = await res.json();
            removeTypingIndicator();

            if (data.reply) {
                appendMessage('assistant', data.reply);
                if (data.session_id) {
                    sessionId = data.session_id;
                    localStorage.setItem('smart_travel_chat_session', sessionId);
                }
            } else {
                appendMessage('assistant', "I apologize, but I encountered a temporary network delay. Please try asking again.");
            }
        } catch (err) {
            removeTypingIndicator();
            console.error(err);
            appendMessage('assistant', "Connection error. Please ensure your internet is active and try again.");
        }
    }

    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage(chatInput.value);
        });
    }

    quickPrompts.forEach(btn => {
        btn.addEventListener('click', () => {
            const prompt = btn.getAttribute('data-prompt') || btn.innerText;
            sendMessage(prompt);
        });
    });
});
