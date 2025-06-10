document.addEventListener('DOMContentLoaded', async function () {
    function saveToggleState(sensorId, isChecked) {
        sessionStorage.setItem(`sensor_${sensorId}`, isChecked);
    }

    function getToggleState(sensorId) {
        return sessionStorage.getItem(`sensor_${sensorId}`) === 'true';
    }

    // Xử lý sự kiện toggle
    async function handleToggle(event) {
        const checkbox = event.target;
        const sensorId = checkbox.id;
        const card = checkbox.closest('.card');


        try {
            // Send request to server
            const response = await fetch(`${API_TOGGLE_SENSOR}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sensorId: sensorId,
                    isTurned: checkbox.checked
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update sensor state');
            }

            if (checkbox.checked) {
                card.classList.add('disabled');
                console.log(`${sensorId} is turned ON`);
            } else {
                card.classList.remove('disabled');
                console.log(`${sensorId} is turned OFF`);
            }

            saveToggleState(sensorId, checkbox.checked);
        } catch (error) {
            console.error('Error updating sensor state:', error);
            checkbox.checked = !checkbox.checked; // Revert checkbox state
            card.classList.toggle('disabled'); // Revert card state
            alert('Failed to update sensor state. Please try again.');
        }
    }

    // Hàm tải trạng thái cảm biến
    async function initializeTogglesFromServer() {
        try {
            const response = await fetch(`${API_GET_SENSOR_STATUS}`);
            if (!response.ok) throw new Error('Failed to fetch sensor states');

            const sensorStates = await response.json();
            console.log('Sensor states from server:', sensorStates);

            const toggles = document.querySelectorAll('.sensor-toggle');
            toggles.forEach(toggle => {
                const sensorId = toggle.id;
                const card = toggle.closest('.card');
                const stateFromServer = sensorStates.find(s => s.sensorId === sensorId);
                console.log(stateFromServer)
                if (stateFromServer) {
                    toggle.checked = stateFromServer.isTurned;
                    if (toggle.checked) {
                        card.classList.remove('disabled');
                    } else {
                        card.classList.add('disabled');
                    }
                    saveToggleState(sensorId, toggle.checked);
                }

                // Thêm event listener sau khi đã set trạng thái
                toggle.addEventListener('change', handleToggle);
            });

        } catch (error) {
            console.error('Failed to load sensor states:', error);
            alert('Không thể tải trạng thái cảm biến từ server.');
        }
    }
    // Hàm tải thông tin người dùng từ server
    async function updateUserTable() {
        try {
            const response = await fetch(`${API_GET_USER_LIST}`);
            if (!response.ok) throw new Error('Failed to fetch user list');

            const data = await response.json();
            if (!data.success || !data.users) {
                alert('Không thể tải thông tin người dùng từ server.');
                return;
            }

            const users = data.users;
            console.log('Users from server:', users);

            const tbody = document.querySelector('.info-table tbody');
            tbody.innerHTML = '';

            users.forEach(user => {
                const tr = document.createElement('tr');
                const userName = document.createElement('td');
                userName.textContent = user.username;

                const emailTd = document.createElement('td');
                emailTd.textContent = user.email;

                const phoneTd = document.createElement('td');
                phoneTd.textContent = user.phone;

                const statusTd = document.createElement('td');
                statusTd.textContent = user.status === 'online' ? 'Active' : 'Inactive';
                statusTd.className = `status ${user.status === 'online' ? 'active' : 'inactive'}`;

                const lastLogin = document.createElement('td');
                lastLogin.textContent = user.lastLogin;

                tr.appendChild(userName)
                tr.appendChild(emailTd);
                tr.appendChild(phoneTd);
                tr.appendChild(statusTd);
                tr.appendChild(lastLogin);

                tbody.appendChild(tr);
            });

        } catch (error) {
            console.error('Failed to load user table:', error);
            alert('Không thể tải thông tin người dùng từ server.');
        }
    }
    async function fetchChatHistory() {
        try {
            // console.log('Fetching chat history...');
            const response = await fetch(`${API_CHAT_HISTORY}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.status === 404) {
                console.warn('No chat history found');
                const tbody = document.querySelector("#chat-history-table tbody");
                if (tbody) {
                    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No chat history available</td></tr>';
                }
                return;
            }

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const csvText = await response.text();
            // console.log('Received CSV text:', csvText.substring(0, 200) + '...'); // Log first 200 chars

            if (!csvText.trim()) {
                console.warn('Received empty CSV data');
                return;
            }

            // Parse CSV using Papa Parse
            Papa.parse(csvText, {
                header: true,
                skipEmptyLines: true,
                transformHeader: header => header.toLowerCase().replace(/\s+/g, '_'),
                complete: function (results) {
                    // console.log('Parsed CSV data:', results.data);
                    const tbody = document.querySelector("#chat-history-table tbody");
                    if (!tbody) {
                        console.error('Could not find chat history table body element');
                        return;
                    }

                    tbody.innerHTML = ""; // Clear existing rows

                    if (results.data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No chat history available</td></tr>';
                        return;
                    }

                    results.data.forEach((row, index) => {
                        // console.log(`Processing row ${index}:`, row);
                        const tr = document.createElement("tr");
                        tr.innerHTML = `
                            <td>${row.timestamp || ''}</td>
                            <td>${row.question || ''}</td>
                            <td>${row.answer || ''}</td>
                            <td>${row.rag_used || ''}</td>
                            <td>${row.rag_documents || ''}</td>
                            <td>${row.response_type || ''}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                },
                error: function (error) {
                    console.error('Error parsing CSV:', error);
                    const tbody = document.querySelector("#chat-history-table tbody");
                    if (tbody) {
                        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error parsing chat history: ${error.message}</td></tr>`;
                    }
                }
            });

        } catch (error) {
            console.error("Error fetching chat history:", error);
            const tbody = document.querySelector("#chat-history-table tbody");
            if (tbody) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error loading chat history: ${error.message}</td></tr>`;
            }
        }
    }

    await initializeTogglesFromServer();
    await updateUserTable();
    await fetchChatHistory();
});