const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");
const ragButton = document.querySelector('#toggle-rag');

let isRagOn = false;
let isThinking = false;

const userData = {
    message: null,
};

const chatHistory = [];

const initialInputHeight = messageInput ? messageInput.scrollHeight : 0;

ragButton.addEventListener('click', () => {
    ragButton.classList.toggle('active');
    isRagOn = ragButton.classList.contains('active');
    // console.log("RAG mode:", isRagOn ? "ON" : "OFF");
  });

const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};
// application/
// const generateBotResponse = async (incomingMessageDiv) => {
//     try {
//         // Get the current language
//         // const language = document.documentElement.lang || 'vi';
//         const language = 'vi';
        
//         // Send the message to the server
//         const response = await fetch('http://localhost:8000/api/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 message: userData.message,
//                 language: language
//             }),
//         });
//         // console.log(response);
//         // Kiểm tra phản hồi có rỗng không
//         if (!response.ok) {
//             throw new Error(`Server error: ${response.status} ${response.statusText}`);
//         }

//         // Kiểm tra phản hồi có nội dung trước khi gọi .json()
//         const text = await response.text();
//         if (!text) {
//             throw new Error("Empty response from server.");
//         }

//         const data = JSON.parse(text);
//         // console.log("data" ,data);
//         // const data = await response.json();
//         // Handle the response
//         if (response.ok) {
//             // Replace the thinking indicator with the actual response
//             const botResponse = (String)(data.response);
//             incomingMessageDiv.classList.remove("thinking");
//             incomingMessageDiv.querySelector(".message-text").innerHTML = botResponse.replace(/\n/g, '<br>');
            
//             // Add to chat history
//             chatHistory.push({
//                 sender: "user",
//                 message: userData.message
//             });
//             chatHistory.push({
//                 sender: "bot",
//                 message: botResponse
//             });
//         } else {
//             // Handle error
//             incomingMessageDiv.classList.remove("thinking");
//             incomingMessageDiv.querySelector(".message-text").innerHTML = data.response || "Sorry, an error occurred.";
//         }
//     } catch (error) {
//         console.error("Error communicating with the server:", error);
//         incomingMessageDiv.classList.remove("thinking");
//         incomingMessageDiv.querySelector(".message-text").innerHTML = "Sorry, I couldn't connect to the server. Please try again later.";
//     }
    
//     // Scroll to the bottom of the chat
//     chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
// };

const generateBotResponse = async (incomingMessageDiv) => {
    try {
        const response = await fetch('http://localhost:8000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userData.message,
                rag: isRagOn
            }),
        });

        if (!response.ok || !response.body) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let botResponse = "";

        // Xóa hiệu ứng thinking
        incomingMessageDiv.classList.remove("thinking");

        // Đọc từng chunk và hiển thị
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            botResponse += chunk;

            // Hiển thị từng phần của chunk
            incomingMessageDiv.querySelector(".message-text").innerHTML = botResponse.replace(/\n/g, "<br>");
            
        }

        // Sau khi hoàn tất, lưu vào history
        chatHistory.push({
            sender: "user",
            message: userData.message
        });
        chatHistory.push({
            sender: "bot",
            message: botResponse
        });
        isThinking = false;
        ragButton.classList.remove('disabled')
        sendMessageButton.classList.remove('disabled')
    } catch (error) {
        console.error("Error communicating with the server:", error);
        incomingMessageDiv.classList.remove("thinking");
        incomingMessageDiv.querySelector(".message-text").innerHTML = "Sorry, I couldn't connect to the server. Please try again later.";
    }
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
};


// Xử lý tin nhắn đi của người dùng
const handleOutgoingMessage = (e) => {
    e.preventDefault();
    if (!messageInput) return;
    
    userData.message = messageInput.value.trim();
    if (!userData.message) return;
    
    messageInput.value = "";
    messageInput.dispatchEvent(new Event("input"));

    const messageContent = `<div class="message-text">${userData.message}</div>`;
    const outGoingMessageDiv = createMessageElement(messageContent, "user-message");
    outGoingMessageDiv.querySelector(".message-text").textContent = userData.message;
    chatBody.appendChild(outGoingMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth"});

    setTimeout(() => {
        const messageContent = `<svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 1024 1024">
                    <path d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5zM867.2 644.5V453.1h26.5c19.4 0 35.1 15.7 35.1 35.1v121.1c0 19.4-15.7 35.1-35.1 35.1h-26.5zM95.2 609.4V488.2c0-19.4 15.7-35.1 35.1-35.1h26.5v191.3h-26.5c-19.4 0-35.1-15.7-35.1-35.1zM561.5 149.6c0 23.4-15.6 43.3-36.9 49.7v44.9h-30v-44.9c-21.4-6.5-36.9-26.3-36.9-49.7 0-28.6 23.3-51.9 51.9-51.9s51.9 23.3 51.9 51.9z"></path>
                </svg>
                <div class="message-text">
                    <div class="thinking-indicator">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>`;
        const incomingMessageDiv = createMessageElement(messageContent, "bot-message", "thinking");
        chatBody.appendChild(incomingMessageDiv);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth"});
        generateBotResponse(incomingMessageDiv);
    }, 600);
};

// Add event listeners if the elements exist
if (messageInput) {
    messageInput.addEventListener("keydown", (e) => {
        const userMessage = e.target.value.trim();
        if(!isThinking && e.key === "Enter" && userMessage && !e.shiftKey && window.innerWidth > 768){
            isThinking = true;
            ragButton.classList.add('disabled')
            sendMessageButton.classList.add('disabled')
            handleOutgoingMessage(e);
        }
        if (isThinking && e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Chặn gửi tin nhắn
        }
    });

    messageInput.addEventListener("input", () => {
        messageInput.style.height = `${initialInputHeight}px`;
        messageInput.style.height = `${messageInput.scrollHeight}px`;
        const chatForm = document.querySelector(".chat-form");
        if (chatForm) {
            chatForm.style.borderRadius = messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
        }
    });
}

if (sendMessageButton) {
    sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e));
}

if (chatbotToggler) {
    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
}

if (closeChatbot) {
    closeChatbot.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
}


