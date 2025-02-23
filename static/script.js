document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
        let tooltips = document.querySelectorAll(".tooltip-text");
        tooltips.forEach(tooltip => {
            if (!tooltip.contains(event.target) && !tooltip.previousElementSibling.contains(event.target)) {
                tooltip.style.visibility = "hidden";
                tooltip.style.opacity = "0";
            }
        });
    });
});

function toggleTooltip(icon) {
    let tooltip = icon.nextElementSibling;
    let rect = icon.getBoundingClientRect();

    // Adjust position so tooltip appears properly
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + "px";
    tooltip.style.left = (rect.left + window.scrollX + 10) + "px";

    if (tooltip.style.visibility === "visible") {
        tooltip.style.visibility = "hidden";
        tooltip.style.opacity = "0";
    } else {
        tooltip.style.visibility = "visible";
        tooltip.style.opacity = "1";
    }
}


// Function to Run Ramdon Test with popular websites
function fillRandomSite() {
    const testSites = [
        "https://www.wp-rocket.me",
        "https://www.cloudflare.com",
        "https://www.google.com",
        "https://www.wordpress.com",
        "https://www.github.com"
        
    ];
    let randomSite = testSites[Math.floor(Math.random() * testSites.length)];
    document.getElementById("url").value = randomSite;
}
