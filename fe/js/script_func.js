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
