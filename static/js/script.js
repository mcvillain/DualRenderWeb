document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('urlForm');
    const content1 = document.getElementById('content1');
    const content2 = document.getElementById('content2');
    const errorDiv = document.getElementById('error');
    const resizeHandle = document.getElementById('resize-handle');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await fetchContent();
    });

    async function fetchContent() {
        const url1 = document.getElementById('url1').value;
        const url2 = document.getElementById('url2').value;

        try {
            const response = await fetch('/fetch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    url1: url1,
                    url2: url2
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            content1.innerHTML = data.content1;
            content2.innerHTML = data.content2;
            errorDiv.textContent = '';

            // Apply styles to rendered content
            applyStylesToContent(content1);
            applyStylesToContent(content2);
        } catch (error) {
            errorDiv.textContent = `Error: ${error.message}`;
        }
    }

    function applyStylesToContent(container) {
        const styles = `
            body { font-family: Arial, sans-serif; }
            img { max-width: 100%; height: auto; }
            a { color: #0066cc; text-decoration: none; }
            a:hover { text-decoration: underline; }
        `;
        const styleElement = document.createElement('style');
        styleElement.textContent = styles;
        container.appendChild(styleElement);
    }

    // Resizing functionality
    let isResizing = false;
    let startX;
    let startWidth;

    resizeHandle.addEventListener('mousedown', (e) => {
        isResizing = true;
        startX = e.clientX;
        startWidth = content1.offsetWidth;
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        const diff = e.clientX - startX;
        content1.style.width = `${startWidth + diff}px`;
        content2.style.width = `calc(100% - ${startWidth + diff}px - 10px)`;
    });

    document.addEventListener('mouseup', () => {
        isResizing = false;
    });

    // Periodically update content
    setInterval(fetchContent, 60000); // Update every 60 seconds
});
