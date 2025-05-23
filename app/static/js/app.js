// Main application file
document.addEventListener('DOMContentLoaded', () => {
    // Initialize PDF handler
    const pdfHandler = new PDFHandler();
    
    // Initialize chat handler
    const chatHandler = new ChatHandler();
    
    // Connect the handlers
    pdfHandler.onSummaryGenerated = (summary) => {
        chatHandler.onNewSummary(summary);
    };

    // PDF Upload Elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('pdf-file');
    const uploadBtn = document.getElementById('upload-btn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    const summaryText = document.getElementById('summary-text');
    const originalLength = document.getElementById('original-length');
    const summaryLength = document.getElementById('summary-length');
    const downloadBtn = document.getElementById('download-btn');

    // Chat Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');

    // PDF Upload Functionality
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', handleFileSelect);

    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('border-blue-500');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('border-blue-500');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('border-blue-500');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    }

    function handleFile(file) {
        if (!file.name.endsWith('.pdf')) {
            showError('Please select a PDF file');
            return;
        }

        // Show loading state
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        error.classList.add('hidden');

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        // Upload file
        fetch('/api/summarize', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.classList.add('hidden');
            
            if (data.error) {
                showError(data.error);
                return;
            }

            // Display results
            summaryText.textContent = data.summary;
            originalLength.textContent = `${data.original_length} characters`;
            summaryLength.textContent = `${data.summary_length} characters`;
            results.classList.remove('hidden');

            // Setup download button
            downloadBtn.onclick = () => {
                const blob = new Blob([data.summary], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'summary.txt';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            };
        })
        .catch(err => {
            loading.classList.add('hidden');
            showError('An error occurred while processing your file');
            console.error('Error:', err);
        });
    }

    function showError(message) {
        error.textContent = message;
        error.classList.remove('hidden');
    }

    // Chat Functionality
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 ${isUser ? 'text-right' : 'text-left'}`;
        
        const messageBubble = document.createElement('div');
        messageBubble.className = `inline-block p-3 rounded-lg ${
            isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
        }`;
        messageBubble.textContent = message;
        
        messageDiv.appendChild(messageBubble);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage(message) {
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
                addMessage('Error: ' + data.error);
            } else {
                addMessage(data.response);
            }
        } catch (error) {
            addMessage('Error: Could not connect to the server');
        }
    }

    async function handleVoiceInput() {
        try {
            const response = await fetch('/api/voice', {
                method: 'POST',
            });

            const data = await response.json();
            
            if (data.error) {
                addMessage('Error: ' + data.error);
            } else {
                addMessage(data.response);
            }
        } catch (error) {
            addMessage('Error: Could not connect to the server');
        }
    }

    // Chat Event Listeners
    sendBtn.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            sendMessage(message);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = userInput.value.trim();
            if (message) {
                addMessage(message, true);
                sendMessage(message);
                userInput.value = '';
            }
        }
    });

    voiceBtn.addEventListener('click', () => {
        handleVoiceInput();
    });
}); 