function fetchEvents() {
    fetch('/events')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('events-container');
            container.innerHTML = '';

            if (data.length === 0) {
                container.innerHTML = '<p class="empty-message">No events yet</p>';
                return;
            }

            data.forEach(event => {
                const div = document.createElement('div');
                div.className = `event-entry ${event.action}`;

                let message = '';
                const timestamp = new Date(event.timestamp).toLocaleString();

                // Formatting based on spec
                if (event.action === 'PUSH') {
                    message = `<strong>${event.author}</strong> pushed to <strong>${event.to_branch}</strong>`;
                } else if (event.action === 'PULL_REQUEST') {
                    message = `<strong>${event.author}</strong> submitted a pull request from <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong>`;
                } else if (event.action === 'MERGE') {
                    message = `<strong>${event.author}</strong> merged branch <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong>`;
                } else {
                    message = `Unknown action: ${event.action}`;
                }

                div.innerHTML = `
                    <div>${message}</div>
                    <span class="timestamp">${timestamp}</span>
                `;
                container.appendChild(div);
            });
        })
        .catch(err => console.error('Error fetching events:', err));
}

// Poll every 15 seconds
setInterval(fetchEvents, 15000);

// Initial load
fetchEvents();
