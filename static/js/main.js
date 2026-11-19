// PokéML Studio - Interactive Client Logic

document.addEventListener("DOMContentLoaded", () => {
    const hpInput = document.getElementById("hp");
    const attackInput = document.getElementById("attack");
    const defenseInput = document.getElementById("defense");
    const heightInput = document.getElementById("height");
    const weightInput = document.getElementById("weight");
    const expInput = document.getElementById("base_experience");
    const type1Select = document.getElementById("type_1");
    const type2Select = document.getElementById("type_2");

    const badgeHp = document.getElementById("badge-hp");
    const badgeAttack = document.getElementById("badge-attack");
    const badgeDefense = document.getElementById("badge-defense");
    const badgeHeight = document.getElementById("badge-height");
    const badgeWeight = document.getElementById("badge-weight");
    const badgeExp = document.getElementById("badge-exp");
    const totalStatsEl = document.getElementById("total-stats");
    const tierHintEl = document.getElementById("stat-tier-hint");

    // Update Live Badges & Stat Total
    function updateLiveStats() {
        if (!hpInput || !attackInput || !defenseInput) return;

        const hp = parseFloat(hpInput.value) || 0;
        const attack = parseFloat(attackInput.value) || 0;
        const defense = parseFloat(defenseInput.value) || 0;
        const height = parseFloat(heightInput?.value) || 0;
        const weight = parseFloat(weightInput?.value) || 0;
        const exp = parseFloat(expInput?.value) || 0;

        if (badgeHp) badgeHp.textContent = hp;
        if (badgeAttack) badgeAttack.textContent = attack;
        if (badgeDefense) badgeDefense.textContent = defense;
        if (badgeHeight) badgeHeight.textContent = `${height} dm (${(height / 10).toFixed(1)}m)`;
        if (badgeWeight) badgeWeight.textContent = `${weight} hg (${(weight / 10).toFixed(1)}kg)`;
        if (badgeExp) badgeExp.textContent = exp;

        const total = Math.round(hp + attack + defense);
        if (totalStatsEl) totalStatsEl.textContent = total;

        if (tierHintEl) {
            if (total >= 280) {
                tierHintEl.className = "badge bg-danger text-light";
                tierHintEl.textContent = "High Attack / Elite Tier (BST: " + total + ")";
            } else if (total >= 190) {
                tierHintEl.className = "badge bg-warning text-dark";
                tierHintEl.textContent = "Medium Attack / Balanced Tier (BST: " + total + ")";
            } else {
                tierHintEl.className = "badge bg-info text-dark";
                tierHintEl.textContent = "Low Attack / Rookie Tier (BST: " + total + ")";
            }
        }
    }

    // Attach input listeners
    [hpInput, attackInput, defenseInput, heightInput, weightInput, expInput].forEach(inp => {
        if (inp) {
            inp.addEventListener("input", updateLiveStats);
        }
    });

    // Preset button handlers
    const presetButtons = document.querySelectorAll(".preset-btn");
    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const hp = btn.getAttribute("data-hp");
            const attack = btn.getAttribute("data-attack");
            const defense = btn.getAttribute("data-defense");
            const height = btn.getAttribute("data-height");
            const weight = btn.getAttribute("data-weight");
            const exp = btn.getAttribute("data-exp");
            const type1 = btn.getAttribute("data-type1");
            const type2 = btn.getAttribute("data-type2");

            if (hpInput) hpInput.value = hp;
            if (attackInput) attackInput.value = attack;
            if (defenseInput) defenseInput.value = defense;
            if (heightInput) heightInput.value = height;
            if (weightInput) weightInput.value = weight;
            if (expInput) expInput.value = exp;

            if (type1Select && type1) {
                type1Select.value = type1;
            }
            if (type2Select && type2) {
                type2Select.value = type2;
            }

            // Visual feedback
            presetButtons.forEach(b => b.classList.remove("active", "btn-danger"));
            btn.classList.add("btn-danger");

            updateLiveStats();
        });
    });

    // Randomize Button
    const randomBtn = document.getElementById("btn-random");
    if (randomBtn) {
        randomBtn.addEventListener("click", () => {
            if (hpInput) hpInput.value = Math.floor(Math.random() * (130 - 35 + 1)) + 35;
            if (attackInput) attackInput.value = Math.floor(Math.random() * (140 - 30 + 1)) + 30;
            if (defenseInput) defenseInput.value = Math.floor(Math.random() * (130 - 30 + 1)) + 30;
            if (heightInput) heightInput.value = Math.floor(Math.random() * (25 - 4 + 1)) + 4;
            if (weightInput) weightInput.value = Math.floor(Math.random() * (1500 - 50 + 1)) + 50;
            if (expInput) expInput.value = Math.floor(Math.random() * (280 - 60 + 1)) + 60;

            if (type1Select) type1Select.value = "auto";
            if (type2Select) type2Select.value = "none";

            updateLiveStats();
        });
    }

    // Initial calculation on page load
    updateLiveStats();
});
