// Chat handling functionality
class ChatHandler {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.voiceBtn = document.getElementById('voice-btn');

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.sendBtn.addEventListener('click', () => this.handleSend());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSend();
            }
        });
        this.voiceBtn.addEventListener('click', () => this.handleVoiceInput());
    }

    handleSend() {
        const message = this.userInput.value.trim();
        if (message) {
            this.addMessage(message, true);
            this.sendMessage(message);
            this.userInput.value = '';
        }
    }

    addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 ${isUser ? 'text-right' : 'text-left'}`;
        
        const messageBubble = document.createElement('div');
        messageBubble.className = `inline-block p-3 rounded-lg ${
            isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
        }`;
        messageBubble.textContent = message;
        
        messageDiv.appendChild(messageBubble);
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            
            if (data.error) {
                this.addMessage('Error: ' + data.error);
            } else {
                this.addMessage(data.response);
            }
        } catch (error) {
            this.addMessage('Error: Could not connect to the server');
        }
    }

    async handleVoiceInput() {
        try {
            const response = await fetch('/api/voice', {
                method: 'POST',
            });

            const data = await response.json();
            
            if (data.error) {
                this.addMessage('Error: ' + data.error);
            } else {
                this.addMessage(data.response);
            }
        } catch (error) {
            this.addMessage('Error: Could not connect to the server');
        }
    }

    // Method to handle new PDF summaries
    onNewSummary(summary) {
        this.addMessage(`New PDF summary available: ${summary.substring(0, 100)}...`);
    }
}

// Export for use in other files
window.ChatHandler = ChatHandler; 