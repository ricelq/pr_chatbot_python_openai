const messageInput = document.getElementById("messageInput");
const buttonText = document.getElementById("buttonText");
const loadingSpinner = document.getElementById("loadingSpinner");
// let history = []; // this will store the conversation history
let history = JSON.parse(getCookie("chatHistory")) || []; // Load history from cookie or initialize as empty array

messageInput.focus();
document.querySelectorAll("pre code").forEach((block) => {
  hljs.highlightElement(block);
});

document.addEventListener("DOMContentLoaded", function () {
  // Load history and display messages
  history.forEach((item) => {
    if (item.role === "user") {
      appendMessage("You", item.content);
    } else {
      appendMessage("Chatbot", item.content);
    }
  });
});

function setLinkTargets() {
  const links = document.querySelectorAll("#chat-box a"); // Assuming your chat box has the ID 'chat-box'
  links.forEach((link) => {
    link.target = "_blank";
  });
}

// Call this function after updating the chat box content
setLinkTargets();

messageInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

function showSpinner(toShow = true) {
  if (toShow) {
    buttonText.classList.add("hidden");
    loadingSpinner.classList.remove("hidden");
  } else {
    buttonText.classList.remove("hidden");
    loadingSpinner.classList.add("hidden");
  }
}

function openFlashMessage(message) {
  const messageContainer = document.getElementById("messageContainer");
  messageContainer.querySelector("#messageValue").textContent = message;
  messageContainer.classList.remove("hidden");
  setTimeout(() => {
    messageContainer.classList.add("hidden");
  }, 2000);
}

function sendMessage() {
  if (!loadingSpinner.classList.contains("hidden")) {
    return false;
  }

  showSpinner();

  let message = messageInput.value.trim();
  if (message == "") {
    openFlashMessage("Please enter a message before sending.");

    setTimeout(() => {
      showSpinner(false);
    }, 500);
  } else {
    const messages = [
      {
        role: "user",
        content: messageInput.value,
      },
    ];

    appendMessage("You", message);

    // apend user message to history
    history.push({ role: "user", content: messageInput.value });

    // save updated history to cookie
    setCookie("chatHistory", JSON.stringify(history), 7);

    fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ messages: messages }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          openFlashMessage("Something wrong!");
          showSpinner(false);
        } else {
          appendMessage("Chatbot", data.response);

          messageInput.value = "";

          // append assistant's response to the history
          history.push({ role: "assistant", content: data.response });

          // Save updated history to cookie
          setCookie("chatHistory", JSON.stringify(history), 7); // Expires in 7 days

          showSpinner(false);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        messageInput.value = "";
      });
  }
}

// Append a message to the chat box
function appendMessage(sender, message) {
  var chatBox = document.getElementById("chat-box");
  var msgHtml;

  if (sender === "You") {
    msgHtml = `<div class="message text-user"><strong>${sender}:</strong> ${message}</div>`;
  } else if (sender === "Chatbot") {
    msgHtml = `<div class="message"><pre><strong>${sender}:</strong><code>${message}</code></pre></div>`;
  }

  chatBox.innerHTML += msgHtml;
  chatBox.scrollTop = chatBox.scrollHeight;

  // Highlight all code blocks if new code is added
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });
}

// Update the response code in the response code box
function updateResponse(code) {
  const responseCode = document.getElementById("responseCode");
  responseCode.textContent = code;
  setTimeout(highlightCode, 100);
}

// Highlight all code blocks in the response code box
function highlightCode() {
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });
}

function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
  let nameEQ = name + "=";
  let ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}
