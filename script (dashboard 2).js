// =========================================
// CAPITAL OPTIMIZER - FRONTEND
// =========================================


// =========================================
// ELEMENTS
// =========================================

const addAssetButton = document.getElementById("addAssetButton");
const assetTable = document.getElementById("assetTable");
const optimizeButton = document.getElementById("optimizeButton");
const simulateButton = document.getElementById("simulateButton");


// =========================================
// ADD ASSET
// =========================================

addAssetButton.addEventListener("click", function () {

    const tbody = assetTable.querySelector("tbody");

    const newRow = tbody.insertRow();

    newRow.innerHTML = `
        <td>
            <input type="text" placeholder="e.g. Gold">
        </td>

        <td>
            <input type="number" placeholder="%">
        </td>

        <td>
            <input type="number" placeholder="%">
        </td>

        <td>
            <input type="number" placeholder="%">
        </td>

        <td>
            <input type="number" placeholder="%">
        </td>

        <td>
            <input type="number" placeholder="0-100">
        </td>
    `;

    updateScenarioAssets();
});


// =========================================
// READ USER INPUT
// =========================================

function getPortfolioInput() {

    const capital =
        document.getElementById("capital").value;

    const rows =
        assetTable.querySelectorAll("tbody tr");

    const assets = [];

    rows.forEach(function (row) {

        const inputs =
            row.querySelectorAll("input");

        const name = inputs[0].value.trim();

        if (name !== "") {

            assets.push({
                name: name,
                currentAllocation: inputs[1].value,
                expectedReturn: inputs[2].value,
                volatility: inputs[3].value,
                maxAllocation: inputs[4].value,
                liquidity: inputs[5].value
            });

        }

    });


    const riskControls = {

        priceShockThreshold:
            document.getElementById(
                "shockThreshold"
            ).value,

        minimumLiquidity:
            document.getElementById(
                "minimumLiquidity"
            ).value,

        rebalanceThreshold:
            document.getElementById(
                "rebalanceThreshold"
            ).value,

        maximumTransactionCost:
            document.getElementById(
                "maximumTransactionCost"
            ).value

    };


    return {

        capital: capital,

        assets: assets,

        riskControls: riskControls

    };
}


// =========================================
// UPDATE SCENARIO ASSET DROPDOWN
// =========================================

function updateScenarioAssets() {

    const select =
        document.getElementById("scenarioAsset");

    const rows =
        assetTable.querySelectorAll("tbody tr");

    select.innerHTML = `
        <option value="">
            Select an asset
        </option>
    `;


    rows.forEach(function (row) {

        const nameInput =
            row.querySelector("input");

        const name =
            nameInput.value.trim();


        if (name !== "") {

            const option =
                document.createElement("option");

            option.value = name;
            option.textContent = name;

            select.appendChild(option);

        }

    });

}


// =========================================
// OPTIMIZE BUTTON
// =========================================

optimizeButton.addEventListener("click", function () {

    const portfolio =
        getPortfolioInput();


    // Basic input check
    if (portfolio.assets.length === 0) {

        alert(
            "Please enter at least one asset."
        );

        return;

    }


    /*
        IMPORTANT:

        The frontend does NOT calculate the
        portfolio optimization.

        The Python backend will do that.

        This section is currently only a
        placeholder until the API is connected.
    */


    // Summary
    document.getElementById("summaryCapital")
        .textContent =
        portfolio.capital
            ? "₹" +
              Number(portfolio.capital)
                  .toLocaleString("en-IN")
            : "—";


    document.getElementById("summaryReturn")
        .textContent = "Awaiting backend";


    document.getElementById("summaryRisk")
        .textContent = "Awaiting backend";


    document.getElementById("summaryLiquidity")
        .textContent = "Awaiting backend";


    // Optimization results

    document.getElementById("resultReturn")
        .textContent = "Awaiting backend";


    document.getElementById("resultVolatility")
        .textContent = "Awaiting backend";


    document.getElementById("resultSharpe")
        .textContent = "Awaiting backend";


    document.getElementById("resultLiquidity")
        .textContent = "Awaiting backend";


    document.getElementById("resultCost")
        .textContent = "Awaiting backend";


    // Allocation section

    document.getElementById("allocationResults")
        .innerHTML = `
            <p class="empty-message">
                Portfolio submitted.
                Recommended allocation will appear
                when the optimization engine is connected.
            </p>
        `;


    // Risk monitor

    document.getElementById("riskBadge")
        .textContent = "AWAITING BACKEND";


    document.getElementById("riskLevel")
        .textContent = "Awaiting backend";


    document.getElementById("riskVolatility")
        .textContent = "Awaiting backend";


    document.getElementById("riskLiquidity")
        .textContent = "Awaiting backend";


    document.getElementById("riskAlerts")
        .innerHTML = `
            <p class="empty-message">
                Risk analysis will appear here
                after the security module is connected.
            </p>
        `;


    // Automated decision

    document.getElementById("decisionAction")
        .textContent = "AWAITING BACKEND";


    document.getElementById("capitalDeployment")
        .textContent = "Awaiting backend";


    document.getElementById("decisionRebalance")
        .textContent = "Awaiting backend";


    document.getElementById("explanation")
        .textContent =
        "The portfolio has been captured by the frontend. " +
        "The optimization and risk engines will provide " +
        "the decision once the backend connection is added.";


    /*
        Later, this exact location will contain
        the API request.

        Example:

        fetch("/analyze", {
            method: "POST",
            ...
        });

        We are deliberately NOT adding that yet.
    */


    console.log("Portfolio input captured:", portfolio);

});


// =========================================
// MARKET SHOCK SIMULATOR
// =========================================

simulateButton.addEventListener("click", function () {

    const asset =
        document.getElementById(
            "scenarioAsset"
        ).value;

    const movement =
        document.getElementById(
            "scenarioMovement"
        ).value;


    if (!asset) {

        alert("Please select an asset.");

        return;

    }


    if (movement === "") {

        alert(
            "Please enter a price movement."
        );

        return;

    }


    /*
        The frontend records the scenario,
        but does NOT decide whether it is
        dangerous.

        That decision will eventually come
        from the risk/security backend.
    */


    document.getElementById("scenarioResult")
        .innerHTML = `
            <div class="scenario-result">

                <h3>Scenario Submitted</h3>

                <p>
                    <strong>Asset:</strong>
                    ${asset}
                </p>

                <p>
                    <strong>Price Movement:</strong>
                    ${movement}%
                </p>

                <p>
                    Risk analysis will be provided
                    by the security and risk engine
                    after the backend is connected.
                </p>

            </div>
        `;


    document.getElementById("decisionAction")
        .textContent = "AWAITING BACKEND";


    document.getElementById("explanation")
        .textContent =
        "The market shock scenario has been submitted. " +
        "The risk engine will determine the severity " +
        "and appropriate action.";

});


// =========================================
// INITIAL SETUP
// =========================================

updateScenarioAssets();