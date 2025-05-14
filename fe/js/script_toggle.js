document.addEventListener('DOMContentLoaded', function () {
    // Lưu trạng thái toggle vào localStorage
    function saveToggleState(sensorId, isChecked) {
        localStorage.setItem(`sensor_${sensorId}`, isChecked);
    }

    // Lấy trạng thái toggle từ localStorage
    function getToggleState(sensorId) {
        return localStorage.getItem(`sensor_${sensorId}`) === 'true';
    }

    // Xử lý sự kiện toggle
    async function handleToggle(event) {
        const checkbox = event.target;
        const sensorId = checkbox.id;
        const card = checkbox.closest('.card');

        try {
            // Send request to server
            const response = await fetch('http://localhost:8000/api/sensor/toggle', {
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

    // Khởi tạo trạng thái cho tất cả các toggle
    const toggles = document.querySelectorAll('.sensor-toggle');
    toggles.forEach(toggle => {
        // Kiểm tra xem đã có trạng thái được lưu chưa
        const savedState = localStorage.getItem(`sensor_${toggle.id}`);
        
        if (savedState === null) {
            // Nếu chưa có trạng thái được lưu, mặc định là ON (checked)
            toggle.checked = true;
            saveToggleState(toggle.id, true);
            toggle.closest('.card').classList.remove('disabled');
        } else {
            // Nếu đã có trạng thái được lưu, sử dụng trạng thái đó
            toggle.checked = getToggleState(toggle.id);
            if (toggle.checked) {
                toggle.closest('.card').classList.remove('disabled');
            } else {
                toggle.closest('.card').classList.add('disabled');
            }
        }
        // Thêm event listener
        toggle.addEventListener('change', handleToggle);
    });
});