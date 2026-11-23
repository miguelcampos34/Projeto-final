document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const themeBtn = document.getElementById("theme-toggle");

    // 1. Modo Claro / Escuro
    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const nextTheme = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
            localStorage.setItem("theme", nextTheme);
        });
    }

    function applyTheme(theme) {
        html.setAttribute("data-theme", theme);
        if (themeBtn) {
            themeBtn.textContent = theme === "dark" ? "☀️ Claro" : "🌙 Escuro";
        }
    }

    // 2. Controle de Tamanho de Fonte (Acessibilidade)
    let fontSize = parseInt(localStorage.getItem("fontSize")) || 100;
    html.style.fontSize = `${fontSize}%`;

    document.getElementById("font-increase")?.addEventListener("click", () => {
        if (fontSize < 125) {
            fontSize += 10;
            updateFont();
        }
    });

    document.getElementById("font-decrease")?.addEventListener("click", () => {
        if (fontSize > 85) {
            fontSize -= 10;
            updateFont();
        }
    });

    document.getElementById("font-reset")?.addEventListener("click", () => {
        fontSize = 100;
        updateFont();
    });

    function updateFont() {
        html.style.fontSize = `${fontSize}%`;
        localStorage.setItem("fontSize", fontSize);
    }
});