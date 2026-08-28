async function analyzeTransaction() {

    const transactionId =
        document.getElementById("transactionId").value.trim();

    const amount =
        Number(document.getElementById("amount").value);

    const timeInput =
        document.getElementById("transactionTime").value;


    if (!transactionId) {
        alert("Please enter Transaction ID");
        return;
    }

    if (!amount || amount <= 0) {
        alert("Please enter a valid transaction amount");
        return;
    }

    if (!timeInput) {
        alert("Please select transaction time");
        return;
    }


    const [hours, minutes] =
        timeInput.split(":").map(Number);

    const timeInSeconds =
        (hours * 3600) + (minutes * 60);


    try {

        const response = await fetch(
            "https://ai-payment-intelligence-engine-1.onrender.com/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    transaction_id:
                        transactionId,

                    amount:
                        amount,

                    time:
                        timeInSeconds,
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "API request failed"
            );
        }


        const data =
            await response.json();


        document
            .getElementById("result")
            .classList.remove("hidden");


        document.getElementById("riskScore").textContent =
        data.risk_score;
        const riskScore = Math.max(
        0,
        Math.min(100, Number(data.risk_score))
        );

        const scaleDot = document.querySelector(".scale-dot");

        scaleDot.style.left = `${riskScore}%`;

        document.getElementById("fraudProbability").textContent =
        (data.fraud_probability * 100).toFixed(2) + "%";


        document.getElementById(
            "riskLevel"
        ).textContent =
            data.risk_level;


        document.getElementById(
            "recommendation"
        ).textContent =
            data.recommendation;


        document.getElementById(
            "recommendationCopy"
        ).textContent =
            data.recommendation;


        const scaleFill =
            document.querySelector(".scale-fill");


        const score =
            Math.max(
                0,
                Math.min(
                    100,
                    Number(data.risk_score)
                )
            );


        scaleDot.style.left =
            `${score}%`;

        scaleFill.style.width =
            `${score}%`;


        const factorsContainer =
            document.getElementById(
                "riskFactors"
            );


        factorsContainer.innerHTML = "";


        data.top_risk_factors.forEach(
            factor => {

                const div =
                    document.createElement("div");


                div.className =
                    "factor";


                div.innerHTML = `
                    <strong>
                        ${factor.feature}
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


    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to the AI Risk API. " +
            "Please make sure the backend is running."
        );
    }

}
