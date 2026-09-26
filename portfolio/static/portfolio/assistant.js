(() => {
    const panel = document.querySelector("[data-assistant]");
    if (!panel) return;

    const launcher = document.querySelector("[data-assistant-launcher]");
    const closeButton = panel.querySelector("[data-assistant-close]");
    const form = panel.querySelector("[data-assistant-form]");
    const input = form.querySelector("[name='message']");
    const sendButton = form.querySelector("[data-assistant-send]");
    const conversation = panel.querySelector("[data-assistant-conversation]");
    const status = panel.querySelector("[data-assistant-status]");
    const error = panel.querySelector("[data-assistant-error]");
    const suggestions = [...panel.querySelectorAll("[data-assistant-question]")];
    const avatarSrc = panel.dataset.assistantAvatarSrc;
    const history = [];
    let busy = false;

    launcher.addEventListener("click", () => {
        if (panel.open) return;
        panel.showModal();
        launcher.setAttribute("aria-expanded", "true");
        closeButton.focus();
    });

    function closePanel() {
        if (!panel.open) return;
        panel.close();
        launcher.setAttribute("aria-expanded", "false");
        launcher.focus();
    }

    closeButton.addEventListener("click", closePanel);
    panel.addEventListener("cancel", (event) => {
        event.preventDefault();
        closePanel();
    });

    function addMessage(role, content) {
        const item = document.createElement("li");
        item.className = `assistant-message assistant-message--${role}`;

        if (role === "assistant") {
            const marker = document.createElement("span");
            marker.className = "assistant-message-marker";
            marker.setAttribute("aria-hidden", "true");
            const avatar = document.createElement("img");
            avatar.className = "assistant-avatar";
            avatar.src = avatarSrc;
            avatar.alt = "";
            avatar.width = 32;
            avatar.height = 32;
            marker.append(avatar);
            item.append(marker);
        }

        const body = document.createElement("div");
        body.className = "assistant-message-body";
        const label = document.createElement("span");
        label.className = "visually-hidden";
        label.textContent = role === "assistant" ? "Assistant: " : "You: ";
        body.append(label, document.createTextNode(content));
        item.append(body);
        conversation.append(item);
        conversation.scrollTop = conversation.scrollHeight;
        return item;
    }

    function remember(message, reply) {
        history.push(
            { role: "user", content: message },
            { role: "assistant", content: reply.slice(0, 1000) },
        );
        while (
            history.length > 8 ||
            history.reduce((length, turn) => length + turn.content.length, 0) > 5000
        ) {
            history.splice(0, 2);
        }
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (busy) return;

        const message = input.value.trim();
        if (!message || message.length > 1000) {
            error.textContent = "Enter a question of up to 1,000 characters.";
            error.hidden = false;
            input.focus();
            return;
        }

        busy = true;
        error.hidden = true;
        error.textContent = "";
        status.textContent = "Thinking…";
        input.disabled = true;
        sendButton.disabled = true;
        suggestions.forEach((button) => { button.disabled = true; });
        const userMessage = addMessage("user", message);
        let errorMessage = "The assistant could not answer right now. Please try again.";

        try {
            const response = await fetch(form.dataset.endpoint, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": form.querySelector("[name='csrfmiddlewaretoken']").value,
                },
                body: JSON.stringify({ message, history }),
            });
            const data = await response.json();
            if (!response.ok || typeof data.reply !== "string" || !data.reply.trim()) {
                if (typeof data.error === "string") errorMessage = data.error;
                throw new Error("Assistant request failed");
            }
            addMessage("assistant", data.reply);
            remember(message, data.reply);
            input.value = "";
        } catch {
            userMessage.remove();
            error.textContent = errorMessage;
            error.hidden = false;
        } finally {
            busy = false;
            status.textContent = "";
            input.disabled = false;
            sendButton.disabled = false;
            suggestions.forEach((button) => { button.disabled = false; });
            if (panel.open) input.focus();
        }
    });

    suggestions.forEach((button) => {
        button.addEventListener("click", () => {
            if (busy) return;
            input.value = button.dataset.assistantQuestion;
            form.requestSubmit();
        });
    });
})();
