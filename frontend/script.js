async function analyzeTransaction() {

    const transactionId =
        document
            .getElementById("transactionId")
            .value
            .trim()
            .toUpperCase();

    if (!transactionId) {

        alert("Please enter a Transaction ID.");

        return;
    }


    if (!/^TXN-\d+$/.test(transactionId)) {

        alert(
            "Invalid Transaction ID.\n\n" +
            "Please use format: TXN-000001"
        );

        return;
    }


    const button =
        document.getElementById("analyzeButton");


    try {


        button.disabled = true;

        button.querySelector("span:first-child").textContent =
            "Analyzing...";

        const response = await fetch(
    "https://ai-payment-intelligence-api.onrender.com/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    transaction_id:
                        transactionId

                })
            }
        );

        if (!response.ok) {

            let errorMessage =
                "Unable to analyze transaction.";

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {

                    if (
                        typeof errorData.detail === "string"
                    ) {

                        errorMessage =
                            errorData.detail;

                    } else {

                        errorMessage =
                            errorData.detail.message ||
                            JSON.stringify(errorData.detail);

                    }
                }

            } catch (e) {
                // Ignore JSON parsing error
            }


            throw new Error(errorMessage);
        }


        // -------------------------------------------------
        // Get response
        // -------------------------------------------------

        const data =
            await response.json();


        // -------------------------------------------------
        // Show result section
        // -------------------------------------------------

        document
            .getElementById("result")
            .classList.remove("hidden");


        // -------------------------------------------------
        // Risk score
        // -------------------------------------------------

        const riskScore =
            Math.max(
                0,
                Math.min(
                    100,
                    Number(data.risk_score)
                )
            );


        document
            .getElementById("riskScore")
            .textContent =
                riskScore.toFixed(2);


        // -------------------------------------------------
        // Risk scale
        // -------------------------------------------------

        const scaleDot =
            document.querySelector(".scale-dot");

        const scaleFill =
            document.querySelector(".scale-fill");


        scaleDot.style.left =
            `${riskScore}%`;

        scaleFill.style.width =
            `${riskScore}%`;


        // -------------------------------------------------
        // Fraud probability
        // -------------------------------------------------

        document
            .getElementById("fraudProbability")
            .textContent =
                (
                    Number(data.fraud_probability) * 100
                ).toFixed(2) + "%";


        // -------------------------------------------------
        // Risk level
        // -------------------------------------------------

        document
            .getElementById("riskLevel")
            .textContent =
                data.risk_level;


        // -------------------------------------------------
        // Recommendation
        // -------------------------------------------------

        document
            .getElementById("recommendation")
            .textContent =
                data.recommendation;


        document
            .getElementById("recommendationCopy")
            .textContent =
                data.recommendation;


const decisionIcon =
    document.getElementById("decisionIcon");

if (data.risk_level === "LOW") {

    decisionIcon.textContent = "✓";

} else if (data.risk_level === "MEDIUM") {

    decisionIcon.textContent = "⚠";

} else {

    decisionIcon.textContent = "!";

}

const riskBadge =
    document.getElementById("riskLevel");

riskBadge.classList.remove(
    "risk-low",
    "risk-medium",
    "risk-high"
);


if (data.risk_level === "LOW") {

    riskBadge.classList.add("risk-low");

} else if (data.risk_level === "MEDIUM") {

    riskBadge.classList.add("risk-medium");

} else {

    riskBadge.classList.add("risk-high");

}

        const factorsContainer =
            document.getElementById(
                "riskFactors"
            );


        factorsContainer.innerHTML = "";


        data.top_risk_factors.forEach(
            (factor, index) => {

                const div =
                    document.createElement("div");


                div.className =
                    "factor";


                div.innerHTML = `
                    <strong>
                        ${index + 1}. ${factor.feature}
                    </strong>

                    <br>

                    Impact:
                    ${factor.impact}

                    <br>

                    ${factor.direction}
                `;


                factorsContainer.appendChild(div);

            }
        );


        // -------------------------------------------------
        // Scroll to result
        // -------------------------------------------------

        document
            .getElementById("result")
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    }


    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Could not connect to the AI Risk API."
        );

    }


    finally {

        button.disabled = false;

        button.querySelector("span:first-child").textContent =
            "Analyze Transaction";

    }

}