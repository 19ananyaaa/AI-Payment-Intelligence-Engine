async function analyzeTransaction() {

    const transactionId =
        document.getElementById("transactionId").value.trim();

    const featureText =
        document.getElementById("features").value.trim();

    if (!transactionId) {
        alert("Please enter Transaction ID");
        return;
    }

    if (!featureText) {
        alert("Please enter transaction features");
        return;
    }

    const features = featureText
        .split(",")
        .map(value => Number(value.trim()));

    if (features.length !== 32 || features.some(isNaN)) {
        alert("Please enter exactly 32 valid feature values.");
        return;
    }

    try {

        const response = await fetch(
            "https://ai-payment-intelligence-engine.onrender.com/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    transaction_id: transactionId,
                    features: features
                })
            }
        );

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        // Show result section
        document
            .getElementById("result")
            .classList.remove("hidden");

        // Basic results
        document.getElementById("riskScore").textContent =
            data.risk_score;

        document.getElementById("fraudProbability").textContent =
            (data.fraud_probability * 100).toFixed(2) + "%";

        document.getElementById("riskLevel").textContent =
            data.risk_level;

        document.getElementById("recommendation").textContent =
            data.recommendation;

        document.getElementById("recommendationCopy").textContent = data.recommendation;

        // Risk factors
        const factorsContainer =
            document.getElementById("riskFactors");

        factorsContainer.innerHTML = "";

        data.top_risk_factors.forEach(factor => {

    const div = document.createElement("div");

    div.className = "factor";

    div.innerHTML = `
        <strong>${factor.feature}</strong>
        <br>
        Impact: ${factor.impact}
        <br>
        ${factor.direction}
    `;

    factorsContainer.appendChild(div);
});

    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to the AI Risk API. " +
            "Make sure FastAPI is running."
        );
    }
}