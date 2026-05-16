document.addEventListener("DOMContentLoaded", () => {
    const likeButtons = document.querySelectorAll(".like-btn");

    likeButtons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.getAttribute("data-id");
            try {
                const res = await fetch(`/api/deals/${id}/like`, {
                    method: "POST"
                });
                if (res.ok) {
                    btn.classList.add("liked");
                }
            } catch (e) {
                console.error("Error liking deal", e);
            }
        });
    });
});
