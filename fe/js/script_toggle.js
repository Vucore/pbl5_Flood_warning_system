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


    async function initializeTogglesFromServer() {
        try {
            const response = await fetch(`${API_GET_SENSOR_STATUS}`);
            if (!response.ok) throw new Error('Failed to fetch sensor states');

            const sensorStates = await response.json(); // [{sensorId, isTurned}, ...]

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
                    saveToggleState(sensorId, toggle.checked); // Cập nhật localStorage
                }

                // Thêm event listener sau khi đã set trạng thái
                toggle.addEventListener('change', handleToggle);
            });

        } catch (error) {
            console.error('Failed to load sensor states:', error);
            alert('Không thể tải trạng thái cảm biến từ server.');
        }
    }

    await initializeTogglesFromServer();

    // // Khởi tạo trạng thái cho tất cả các toggle
    // const toggles = document.querySelectorAll('.sensor-toggle');
    // toggles.forEach(toggle => {
    //     // Kiểm tra xem đã có trạng thái được lưu chưa
    //     const savedState = localStorage.getItem(`sensor_${toggle.id}`);
        
    //     if (savedState === null) {
    //         // Nếu chưa có trạng thái được lưu, mặc định là ON (checked)
    //         toggle.checked = true;
    //         saveToggleState(toggle.id, true);
    //         toggle.closest('.card').classList.remove('disabled');
    //     } else {
    //         // Nếu đã có trạng thái được lưu, sử dụng trạng thái đó
    //         toggle.checked = getToggleState(toggle.id);
    //         if (toggle.checked) {
    //             toggle.closest('.card').classList.remove('disabled');
    //         } else {
    //             toggle.closest('.card').classList.add('disabled');
    //         }
    //     }
    //     // Thêm event listener
    //     toggle.addEventListener('change', handleToggle);
    // });
});