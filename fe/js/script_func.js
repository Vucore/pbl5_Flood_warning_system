const openModalBtn = document.getElementById("openModalBtn");
const closeModalBtn = document.getElementById("closeModalBtn");
const registerModal = document.getElementById("registerModal");

const username = document.getElementById("username");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const address = document.getElementById("address");

const registerButton = document.getElementById("register_btn");

document.addEventListener('DOMContentLoaded', function() {
	const warningText = document.getElementById("warning");
	const warningButton = document.getElementById("hide-warning");

	if (warningButton) {
		warningButton.addEventListener("click", function() {
			if (warningText) {
				warningText.style.display = "none";
			}
		});
	}
});

async function sendRegisterData(data) {
	try {
		const response = await fetch(`${API_REGISTER}`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(errorData.message || "Đăng ký thất bại.");
		}

		const result = await response.json();
		return result;

	} catch (error) {
		console.error("Lỗi gửi đăng ký:", error);
		throw error;
	}
}


document.addEventListener("DOMContentLoaded", () => {

	// Hiển thị modal khi nhấn nút "Đăng ký"
	openModalBtn.addEventListener("click", () => {
		registerModal.style.display = "block";
	});

	// Đóng modal khi nhấn nút "X"
	closeModalBtn.addEventListener("click", () => {
		registerModal.style.display = "none";
	});

	// Đóng modal khi nhấn ra ngoài modal
	window.addEventListener("click", (event) => {
		if (event.target === registerModal) {
			registerModal.style.display = "none";
		}
	});

	// Xử lý sự kiện gửi form
	const registerForm = document.getElementById("registerForm");
	registerForm.addEventListener("submit", async (event) => {
		event.preventDefault(); // Ngăn hành vi mặc định của form
	
		// Lấy dữ liệu từ các trường
		const nameVal = username.value.trim();
		const emailVal = email.value.trim();
		const phoneVal = phone.value.trim();
		const addressVal = address.value.trim();
	
		// Kiểm tra dữ liệu
		if (!nameVal || !emailVal || !phoneVal) {
			alert("Vui lòng điền đầy đủ thông tin.");
			return;
		}
	
		const formData = {
			username: nameVal,
			email: emailVal,
			phone: phoneVal,
			address: addressVal
		};
	
		try {
			const result = await sendRegisterData(formData);
			console.log(result)
			if (result)
			{
				alert("✅ Đăng ký thành công!");
				registerForm.reset();
				registerModal.style.display = "none";
			}
			else {
				alert("❌ Đăng ký thất bại. Vui lòng thử lại sau.");
				username.value = "";
				email.value = "";
				phone.value = "";
				address.value = "";
			}
		} catch (err) {
			alert("❌ Đăng ký thất bại. Vui lòng thử lại sau.");
		}
	});
}) 