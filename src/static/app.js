document.addEventListener('DOMContentLoaded', () => {
    // Session Management
    let sessionId = localStorage.getItem('rag_session_id');
    if (!sessionId) {
        sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('rag_session_id', sessionId);
    }
    console.log("Session ID:", sessionId);

    // Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const chatHistory = document.getElementById('chatHistory');
    const userQuery = document.getElementById('userQuery');
    const sendBtn = document.getElementById('sendBtn');
    const docList = document.getElementById('docList');
    const modelSelect = document.getElementById('modelSelect');
    const clearAllBtn = document.getElementById('clearAllBtn');

    // Headers helper
    const getHeaders = () => ({
        'X-Session-ID': sessionId,
        // Content-Type is auto-set for FormData, manually set for JSON if needed
    });

    // --- Model Selection ---
    modelSelect.addEventListener('change', async (e) => {
        const model = e.target.value;
        try {
            await fetch(`/set_model/?model=${model}`, {
                method: 'POST',
                headers: getHeaders()
            });
            showUploadStatus(`Model switched to ${model}`, 'success');
        } catch (e) {
            console.error(e);
        }
    });

    // --- Clear All Button ---
    clearAllBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear all documents? This cannot be undone.')) {
            try {
                const res = await fetch('/documents/clear', {
                    method: 'POST',
                    headers: getHeaders()
                });
                const data = await res.json();
                if (res.ok && data.status === 'success') {
                    docList.innerHTML = '';
                    updateClearButtonVisibility();
                    showUploadStatus('All documents cleared', 'success');
                    addSystemMessage('Knowledge base has been <strong>cleared</strong>. Upload new documents to get started.');
                } else {
                    showUploadStatus('Failed to clear documents', 'error');
                }
            } catch (e) {
                console.error(e);
                showUploadStatus('Error clearing documents', 'error');
            }
        }
    });

    // --- Document List Management ---
    function updateClearButtonVisibility() {
        clearAllBtn.style.display = docList.children.length > 0 ? 'flex' : 'none';
    }

    function addDocToList(filename) {
        const li = document.createElement('li');
        li.className = 'doc-item';
        li.innerHTML = `
            <i data-lucide="file-text" size="14"></i>
            <span>${filename}</span>
            <button class="delete-btn" title="Delete">
                <i data-lucide="trash-2" size="14"></i>
            </button>
        `;

        // Delete Action
        li.querySelector('.delete-btn').addEventListener('click', async () => {
            try {
                const res = await fetch(`/documents/${filename}`, {
                    method: 'DELETE',
                    headers: getHeaders()
                });
                if (res.ok) {
                    li.remove();
                    updateClearButtonVisibility();
                }
            } catch (e) { console.error(e); }
        });

        docList.appendChild(li);
        updateClearButtonVisibility();
        lucide.createIcons();
    }

    // --- File Upload ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        showUploadStatus('Uploading...', 'neutral');

        try {
            const response = await fetch('/ingest/', {
                method: 'POST',
                headers: getHeaders(),
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                showUploadStatus(`Ingested: ${file.name}`, 'success');
                addDocToList(file.name);
                addSystemMessage(`Successfully indexed document: <strong>${file.name}</strong>`);
            } else {
                showUploadStatus(`Error: ${data.detail}`, 'error');
            }
        } catch (error) {
            showUploadStatus(`Network error: ${error.message}`, 'error');
        }
    }

    function showUploadStatus(msg, type) {
        uploadStatus.innerHTML = '';
        const div = document.createElement('div');
        div.className = type === 'success' ? 'success-msg' : type === 'error' ? 'error-msg' : 'status-msg';
        const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'alert-circle' : 'loader';
        div.innerHTML = `<i data-lucide="${icon}"></i> <span>${msg}</span>`;
        uploadStatus.appendChild(div);
        lucide.createIcons();
    }

    // --- Chat ---
    userQuery.addEventListener('input', () => {
        sendBtn.disabled = userQuery.value.trim() === '';
    });

    userQuery.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !sendBtn.disabled) {
            handleSearch();
        }
    });

    sendBtn.addEventListener('click', handleSearch);

    async function handleSearch() {
        const query = userQuery.value.trim();
        if (!query) return;

        addMessage(query, 'user');
        userQuery.value = '';
        sendBtn.disabled = true;

        // Prepare Bot Message Bubble
        const { msgContent, msgDiv } = createBotMessage();

        const startTime = Date.now();

        try {
            const url = new URL('/ask/', window.location.origin);
            url.searchParams.append('query', query);

            const response = await fetch(url, {
                method: 'GET',
                headers: getHeaders()
            });

            if (!response.ok) throw new Error("API Error");

            // Handle Stream
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                fullText += chunk;

                // Simple parser for Source Header vs Content
                let displayText = fullText;
                let sourcesHtml = "";
                let isThinking = false;

                if (fullText.startsWith("Sources: ")) {
                    const splitIdx = fullText.indexOf("\n\n");
                    if (splitIdx !== -1) {
                        const sourceLine = fullText.substring(0, splitIdx);
                        displayText = fullText.substring(splitIdx + 2);

                        const sources = sourceLine.replace("Sources: ", "").split(", ");
                        sourcesHtml = `<div class="source-badges">
                            ${sources.map(s => `<span class="source-badge">${s}</span>`).join('')}
                         </div>`;
                    } else {
                        // Header incomplete, keep thinking state
                        displayText = "";
                        isThinking = true;
                    }
                }

                // If we have sources but no text yet, show thinking dots
                if (!displayText && sourcesHtml) {
                    isThinking = true;
                }

                if (isThinking) {
                    msgContent.innerHTML = `<p class="thinking-text">Thinking<span class="dot-1">.</span><span class="dot-2">.</span><span class="dot-3">.</span></p>` + sourcesHtml;
                } else {
                    msgContent.innerHTML = formatText(displayText) + sourcesHtml;
                }

                scrollToBottom();
            }

            // Add Timer
            const duration = (Date.now() - startTime) / 1000;
            const timeStr = duration < 60 ? `${Math.round(duration)}s` : `${(duration / 60).toFixed(1)}m`;

            const timeSpan = document.createElement('span');
            timeSpan.className = 'msg-timer';
            timeSpan.innerText = timeStr;
            msgDiv.querySelector('.content').appendChild(timeSpan);

        } catch (error) {
            msgContent.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        } finally {
            lucide.createIcons();
        }
    }

    function addMessage(text, role) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        const avatar = role === 'user' ? 'user' : 'bot';
        msgDiv.innerHTML = `
            <div class="avatar"><i data-lucide="${avatar}"></i></div>
            <div class="content"><p>${text}</p></div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
        lucide.createIcons();
    }

    function createBotMessage() {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message bot`;
        msgDiv.innerHTML = `
            <div class="avatar"><i data-lucide="bot"></i></div>
            <div class="content"><p>Thinking...</p></div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
        lucide.createIcons();

        return {
            msgDiv: msgDiv,
            msgContent: msgDiv.querySelector('.content')
        };
    }

    function formatText(text) {
        // Simple formatter
        let out = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        return `<p>${out}</p>`;
    }

    function addSystemMessage(html) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message system`;
        msgDiv.innerHTML = `
            <div class="avatar"><i data-lucide="info"></i></div>
            <div class="content"><p>${html}</p></div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
        lucide.createIcons();
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
