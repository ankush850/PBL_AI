// PDF handling functionality
class PDFHandler {
    constructor() {
        this.uploadArea = document.getElementById('upload-area');
        this.fileInput = document.getElementById('pdf-file');
        this.uploadBtn = document.getElementById('upload-btn');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        this.error = document.getElementById('error');
        this.summaryText = document.getElementById('summary-text');
        this.originalLength = document.getElementById('original-length');
        this.summaryLength = document.getElementById('summary-length');
        this.downloadBtn = document.getElementById('download-btn');

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop handlers
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('border-blue-500');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('border-blue-500');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('border-blue-500');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        if (!file.name.endsWith('.pdf')) {
            this.showError('Please select a PDF file');
            return;
        }

        // Show loading state
        this.loading.classList.remove('hidden');
        this.results.classList.add('hidden');
        this.error.classList.add('hidden');

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
            this.loading.classList.add('hidden');
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            // Display results
            this.summaryText.textContent = data.summary;
            this.originalLength.textContent = `${data.original_length} characters`;
            this.summaryLength.textContent = `${data.summary_length} characters`;
            this.results.classList.remove('hidden');

            // Setup download button
            this.downloadBtn.onclick = () => {
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

            // Notify chat about new summary
            if (window.chatHandler) {
                window.chatHandler.onNewSummary(data.summary);
            }
        })
        .catch(err => {
            this.loading.classList.add('hidden');
            this.showError('An error occurred while processing your file');
            console.error('Error:', err);
        });
    }

    showError(message) {
        this.error.textContent = message;
        this.error.classList.remove('hidden');
    }
}

// Export for use in other files
window.PDFHandler = PDFHandler; 