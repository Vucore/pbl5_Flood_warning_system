async function applyPassword() {
    const passwordInput = document.getElementById("password_input");
    const password = passwordInput.value;
    if (!password) {
        alert("Please enter a password");
        return;
    }

    try {
        const response = await fetch(`${API_ADMIN_PASS}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ password: password }),
        });

        const result = await response.json();

        if (response.ok) {
            alert("Password set successfully!");
            passwordInput.value = "";
        } else {
            alert("Error: " + result.detail || "Failed to set password");
        }
    } catch (error) {
        console.error("Error setting password:", error);
        alert("Server error!");
    }
}
async function applyWaterLevel() {
    const value = document.getElementById("water_level_input").value;
    if (!value || isNaN(value)) {
        alert("Please enter a valid number");
        return;
    }

    try {
        const response = await fetch(`${API_SET_DISTANCE_SENSOR}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ threshold_cm: Number(value) }),
        });

        const result = await response.json();

        if (response.ok) {
            alert("Water level threshold set successfully!");
        } else {
            alert("Error: " + result.detail || "Failed to set threshold");
        }
    } catch (error) {
        console.error("Error setting water level:", error);
        alert("Server error!");
    }
}