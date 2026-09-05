import numpy as np
from scipy.optimize import minimize


# ============================================================
# 1. INPUT VALIDATION
# ============================================================

def validate_inputs(
    assets,
    current_allocations,
    expected_returns,
    volatilities,
    correlations,
    max_allocations,
    liquidity_scores
):
  

    

    

# ============================================================
# 2. CREATE COVARIANCE MATRIX
# ============================================================

def create_covariance_matrix(
    volatilities,
    correlations
):
    """
    Converts volatility + correlation into
    a covariance matrix.

    Covariance is required by Modern Portfolio Theory
    to calculate total portfolio risk.
    """

    volatilities = np.array(
        volatilities,
        dtype=float
    )

    correlations = np.array(
        correlations,
        dtype=float
    )

    covariance_matrix = (
        np.outer(
            volatilities,
            volatilities
        )
        * correlations
    )

    return covariance_matrix


# ============================================================
# 3. PORTFOLIO RETURN
# ============================================================

def calculate_portfolio_return(
    weights,
    expected_returns
):
    """
    Calculates expected portfolio return.

    Formula:

        Portfolio Return = Σ(weight × asset return)
    """

    return np.dot(
        weights,
        expected_returns
    )


# ============================================================
# 4. PORTFOLIO RISK
# ============================================================

def calculate_portfolio_variance(
    weights,
    covariance_matrix
):
    """
    Calculates portfolio variance.

    Formula:

        wᵀΣw
    """

    return np.dot(
        weights.T,
        np.dot(
            covariance_matrix,
            weights
        )
    )


def calculate_portfolio_volatility(
    weights,
    covariance_matrix
):
    """
    Calculates annualized portfolio volatility.
    """

    variance = calculate_portfolio_variance(
        weights,
        covariance_matrix
    )

    return np.sqrt(
        max(variance, 0)
    )


# ============================================================
# 5. SHARPE RATIO
# ============================================================

def calculate_sharpe_ratio(
    weights,
    expected_returns,
    covariance_matrix,
    risk_free_rate
):
    """
    Measures risk-adjusted return.

    Higher Sharpe ratio generally means
    better return relative to risk.
    """

    portfolio_return = calculate_portfolio_return(
        weights,
        expected_returns
    )

    portfolio_volatility = calculate_portfolio_volatility(
        weights,
        covariance_matrix
    )

    if portfolio_volatility == 0:
        return 0

    return (
        portfolio_return - risk_free_rate
    ) / portfolio_volatility


# ============================================================
# 6. LIQUIDITY
# ============================================================

def calculate_liquidity(
    weights,
    liquidity_scores
):
    """
    Calculates weighted portfolio liquidity.

    Liquidity score:

        1.0 = highly liquid
        0.0 = highly illiquid
    """

    return np.dot(
        weights,
        liquidity_scores
    )


# ============================================================
# 7. MPT OPTIMIZATION
# ============================================================

def optimize_portfolio(
    expected_returns,
    covariance_matrix,
    max_allocations,
    liquidity_scores,
    minimum_return,
    minimum_liquidity
):
    """
    Finds the lowest-risk portfolio while satisfying:

    - 100% capital allocation
    - Minimum expected return
    - Minimum liquidity
    - Maximum allocation per asset
    - No short selling

    This is the core Modern Portfolio Theory engine.
    """

    number_of_assets = len(
        expected_returns
    )

    # Start from equal allocation.
    initial_weights = (
        np.ones(number_of_assets)
        / number_of_assets
    )

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    def objective(weights):

        # Minimize portfolio variance.
        return calculate_portfolio_variance(
            weights,
            covariance_matrix
        )

  
    # CONSTRAINTS


    constraints = [

        # Total allocation = 100%
        {
            "type": "eq",

            "fun": lambda weights:
                np.sum(weights) - 1
        },

        # Minimum expected return
        {
            "type": "ineq",

            "fun": lambda weights:
                calculate_portfolio_return(
                    weights,
                    expected_returns
                ) - minimum_return
        },

        # Minimum liquidity
        {
            "type": "ineq",

            "fun": lambda weights:
                calculate_liquidity(
                    weights,
                    liquidity_scores
                ) - minimum_liquidity
        }
    ]

    # ASSET LIMITS
    

    bounds = [
        (
            0,
            max_allocations[i]
        )

        for i in range(number_of_assets)
    ]

    # OPTIMIZE


    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:

        raise ValueError(
            "Optimization failed: "
            + result.message
        )

    return result.x



# 8. VOLATILITY MONITOR


def monitor_volatility(
    assets,
    volatilities
):
    """
    Classifies each asset according to its volatility.

    These thresholds can be changed depending on
    the institution's risk policy.
    """

    results = []

    for asset, volatility in zip(
        assets,
        volatilities
    ):

        if volatility < 0.08:

            risk_level = "LOW"

        elif volatility < 0.15:

            risk_level = "MEDIUM"

        elif volatility < 0.25:

            risk_level = "HIGH"

        else:

            risk_level = "VERY HIGH"

        results.append({

            "asset": asset,

            "volatility_percent":
                round(
                    volatility * 100,
                    2
                ),

            "risk_level":
                risk_level
        })

    return results



# 9. DYNAMIC VOLATILITY SHOCK DETECTION


def detect_volatility_shock(
    normal_volatilities,
    current_volatilities,
    shock_multiplier=1.5
):
    """
    Detects when an asset's current volatility has
    increased significantly compared with its normal level.

    Example:

        Normal volatility = 10%
        Current volatility = 16%

        16 / 10 = 1.6

        Since 1.6 > 1.5,
        a volatility shock is detected.
    """

    shocks = []

    for i in range(
        len(normal_volatilities)
    ):

        normal = normal_volatilities[i]

        current = current_volatilities[i]

        if normal == 0:

            ratio = 0

        else:

            ratio = current / normal

        shocks.append(
            ratio >= shock_multiplier
        )

    return shocks



# 10. REBALANCING DETECTION


def recommend_rebalancing(
    assets,
    current_allocations,
    target_allocations,
    rebalance_threshold
):
    """
    Determines whether the portfolio has drifted enough
    to justify rebalancing.

    Small changes are ignored.

    This helps prevent unnecessary transactions.
    """

    recommendations = []

    for i, asset in enumerate(assets):

        current = current_allocations[i]

        target = target_allocations[i]

        difference = target - current

        if abs(difference) >= rebalance_threshold:

            if difference > 0:

                action = "INCREASE"

            else:

                action = "REDUCE"

            recommendations.append({

                "asset": asset,

                "action": action,

                "current_percent":
                    round(
                        current * 100,
                        2
                    ),

                "target_percent":
                    round(
                        target * 100,
                        2
                    ),

                "change_percent":
                    round(
                        difference * 100,
                        2
                    )
            })

    return recommendations



# 11. TRANSACTION COST CALCULATION


def calculate_transaction_cost(
    current_allocations,
    new_allocations,
    total_capital,
    transaction_rate
):
    """
    Estimates the cost of changing the portfolio.

    This is NOT an actual brokerage calculation.

    It is a simplified simulation:

        Transaction Cost =
        Amount Traded × Transaction Rate
    """

    turnover = np.sum(
        np.abs(
            new_allocations
            - current_allocations
        )
    )

    amount_traded = (
        turnover
        * total_capital
    )

    transaction_cost = (
        amount_traded
        * transaction_rate
    )

    return transaction_cost



# 12. COST-AWARE REBALANCING


def create_cost_aware_rebalance(
    current_allocations,
    target_allocations,
    total_capital,
    transaction_rate,
    maximum_transaction_cost
):
    """
    Attempts to move the portfolio toward its optimized
    allocation without exceeding the transaction-cost budget.

    Important:

        We do NOT force a trade.

        If the optimized portfolio requires too much
        turnover, only part of the adjustment is recommended.
    """

    full_cost = calculate_transaction_cost(
        current_allocations,
        target_allocations,
        total_capital,
        transaction_rate
    )

    # Full adjustment is affordable.
    if full_cost <= maximum_transaction_cost:

        return (
            target_allocations,
            full_cost,
            False
        )

   
    # Reduce the size of the rebalance.


    scale = (
        maximum_transaction_cost
        / full_cost
    )

    adjusted_allocations = (
        current_allocations
        +
        scale
        *
        (
            target_allocations
            - current_allocations
        )
    )

    # Make sure allocations total exactly 100%.
    adjusted_allocations /= np.sum(
        adjusted_allocations
    )

    adjusted_cost = calculate_transaction_cost(
        current_allocations,
        adjusted_allocations,
        total_capital,
        transaction_rate
    )

    return (
        adjusted_allocations,
        adjusted_cost,
        True
    )


# 13. COMPLETE PORTFOLIO ANALYSIS


def analyze_portfolio(
    capital,
    assets,
    current_allocations,
    expected_returns,
    volatilities,
    correlations,
    max_allocations,
    liquidity_scores,
    minimum_return,
    minimum_liquidity,
    risk_free_rate,
    rebalance_threshold,
    transaction_rate,
    maximum_transaction_cost
):
    """
    Main backend function.

    This is the function your API/frontend can eventually call.
    """

   
    # Convert inputs to NumPy arrays
 
    current_allocations = np.array(
        current_allocations,
        dtype=float
    )

    expected_returns = np.array(
        expected_returns,
        dtype=float
    )

    volatilities = np.array(
        volatilities,
        dtype=float
    )

    max_allocations = np.array(
        max_allocations,
        dtype=float
    )

    liquidity_scores = np.array(
        liquidity_scores,
        dtype=float
    )


    # Validate
 

    validate_inputs(
        assets,
        current_allocations,
        expected_returns,
        volatilities,
        correlations,
        max_allocations,
        liquidity_scores
    )

  
    # Covariance matrix
 

    covariance_matrix = create_covariance_matrix(
        volatilities,
        correlations
    )

  
    # Analyze CURRENT portfolio
  

    current_return = calculate_portfolio_return(
        current_allocations,
        expected_returns
    )

    current_volatility = calculate_portfolio_volatility(
        current_allocations,
        covariance_matrix
    )

    current_sharpe = calculate_sharpe_ratio(
        current_allocations,
        expected_returns,
        covariance_matrix,
        risk_free_rate
    )

    current_liquidity = calculate_liquidity(
        current_allocations,
        liquidity_scores
    )

  
    # Find OPTIMAL portfolio
  

    target_allocations = optimize_portfolio(
        expected_returns,
        covariance_matrix,
        max_allocations,
        liquidity_scores,
        minimum_return,
        minimum_liquidity
    )


    # Analyze OPTIMIZED portfolio
 

    target_return = calculate_portfolio_return(
        target_allocations,
        expected_returns
    )

    target_volatility = calculate_portfolio_volatility(
        target_allocations,
        covariance_matrix
    )

    target_sharpe = calculate_sharpe_ratio(
        target_allocations,
        expected_returns,
        covariance_matrix,
        risk_free_rate
    )

    target_liquidity = calculate_liquidity(
        target_allocations,
        liquidity_scores
    )

   
    # Volatility monitoring


    volatility_report = monitor_volatility(
        assets,
        volatilities
    )

    # Rebalancing recommendation


    rebalance_recommendations = recommend_rebalancing(
        assets,
        current_allocations,
        target_allocations,
        rebalance_threshold
    )


    # Cost-aware rebalance
  

    (
        adjusted_allocations,
        transaction_cost,
        cost_limit_reached
    ) = create_cost_aware_rebalance(

        current_allocations,

        target_allocations,

        capital,

        transaction_rate,

        maximum_transaction_cost
    )


    rebalance_required = (
        len(rebalance_recommendations) > 0
    )

    if not rebalance_required:

        decision = (
            "HOLD: Portfolio is sufficiently close "
            "to the optimized allocation. "
            "No unnecessary rebalancing is recommended."
        )

    elif cost_limit_reached:

        decision = (
            "PARTIAL REBALANCE: The optimized portfolio "
            "would exceed the transaction-cost budget. "
            "A smaller adjustment is recommended."
        )

    else:

        decision = (
            "REBALANCE: Portfolio allocation has drifted "
            "significantly from the optimized allocation. "
            "Rebalancing is recommended."
        )

  

    return {

        "capital": capital,

        "current_portfolio": {

            "expected_return_percent":
                round(
                    current_return * 100,
                    2
                ),

            "volatility_percent":
                round(
                    current_volatility * 100,
                    2
                ),

            "sharpe_ratio":
                round(
                    current_sharpe,
                    3
                ),

            "liquidity_score":
                round(
                    current_liquidity,
                    3
                )
        },

        "optimized_portfolio": {

            "expected_return_percent":
                round(
                    target_return * 100,
                    2
                ),

            "volatility_percent":
                round(
                    target_volatility * 100,
                    2
                ),

            "sharpe_ratio":
                round(
                    target_sharpe,
                    3
                ),

            "liquidity_score":
                round(
                    target_liquidity,
                    3
                )
        },

        "optimized_allocation": {

            asset:
                round(
                    target_allocations[i] * 100,
                    2
                )

            for i, asset
            in enumerate(assets)
        },

        "volatility_monitor":
            volatility_report,

        "rebalance_required":
            rebalance_required,

        "rebalance_recommendations":
            rebalance_recommendations,

        "transaction_cost":
            round(
                transaction_cost,
                2
            ),

        "maximum_transaction_cost":
            maximum_transaction_cost,

        "cost_limit_reached":
            cost_limit_reached,

        "adjusted_allocation": {

            asset:
                round(
                    adjusted_allocations[i] * 100,
                    2
                )

            for i, asset
            in enumerate(assets)
        },

        "decision":
            decision
    }




