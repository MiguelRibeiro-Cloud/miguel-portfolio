const screenshotDialog = document.querySelector(".screenshot-dialog");

if (screenshotDialog && typeof screenshotDialog.showModal === "function") {
    const previewImage = screenshotDialog.querySelector(".screenshot-dialog-image");
    const previewCaption = screenshotDialog.querySelector(".screenshot-dialog-caption");
    let opener = null;

    document.querySelectorAll(".screenshot-link").forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            opener = link;
            const thumbnail = link.querySelector("img");
            const caption = link.closest("figure").querySelector("figcaption");

            previewImage.src = link.href;
            previewImage.alt = thumbnail.alt;
            previewCaption.textContent = caption ? caption.textContent.trim() : thumbnail.alt;
            screenshotDialog.showModal();
        });
    });

    screenshotDialog.addEventListener("click", (event) => {
        if (event.target === screenshotDialog) screenshotDialog.close();
    });

    screenshotDialog.addEventListener("close", () => {
        if (opener) opener.focus();
    });
}
