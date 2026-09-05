import numpy as np
from datetime import datetime

def get_float(prompt, minimum=None, maximum=None):

    while True:

        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Value must be >= {minimum}")
                continue

            if maximum is not None and value > maximum:
                print(f"Value must be <= {maximum}")
                continue
            
            return value

        except ValueError:
            print("Please enter a valid number.")


def get_percentage(prompt):

    while True:

        value = get_float(prompt, 0, 100)

        return value / 100

def get_portfolio_input():

    print("\n")
    print("=" * 70)
    print("       AUTOMATED CAPITAL RISK MANAGEMENT SYSTEM")
    print("=" * 70)

    capital = get_float(
        "\nEnter total capital (₹): ",
        minimum=0
    )
    while True:
        try:
            number_of_assets = int(
                input("\nEnter number of assets: ")
            )
            if number_of_assets < 2:
                print("Please enter at least 2 assets.")
                continue
            break
        except ValueError:

            print("Enter a valid integer.")
    assets = {}
    print("\n")
    print("-" * 70)
    print("ENTER ASSET INFORMATION")
    print("-" * 70)

    for i in range(number_of_assets):
        print(f"\nAsset {i + 1}")
        symbol = input(
            "Asset name/symbol: "
        ).strip()
        while symbol in assets:
            print("Asset already entered.")
            symbol = input(
                "Enter a different asset: "
            ).strip()
        current_weight = get_percentage(
            "Current allocation (%): "
        )
        target_weight = get_percentage(
            "Target allocation (%): "
        )
        volatility = get_percentage(
            "Volatility (%): "
        )
        liquidity = get_float(
            "Liquidity score (0-100): ",
            minimum=0,
            maximum=100
        )
        max_allocation = get_percentage(
            "Maximum allowed allocation (%): "
        )
        assets[symbol] = {
            "current_weight": current_weight,

            "target_weight": target_weight,

            "volatility": volatility,

            "liquidity": liquidity,

            "max_allocation": max_allocation
        }
    return capital, assets

def get_risk_parameters():

    print("\n")
    print("-" * 70)
    print("RISK CONTROL PARAMETERS")
    print("-" * 70)

    price_shock_threshold = get_percentage(
        "\nPrice shock threshold (%): "
    )
    portfolio_loss_threshold = get_percentage(
        "Portfolio loss threshold (%): "
    )
    asset_volatility_threshold = get_percentage(
        "High asset volatility threshold (%): "
    )
    medium_volatility = get_percentage(
        "Medium portfolio volatility threshold (%): "
    )
    high_volatility = get_percentage(
        "High portfolio volatility threshold (%): "
    )
    critical_volatility = get_percentage(
        "Critical portfolio volatility threshold (%): "
    )
    minimum_liquidity = get_float(
        "Minimum liquidity score (0-100): ",
        minimum=0,
        maximum=100
    )
    rebalance_threshold = get_percentage(
        "Rebalancing threshold (%): "
    )
    transaction_cost_rate = get_percentage(
        "Transaction cost rate (%): "
    )
    max_transaction_cost = get_float(
        "Maximum transaction cost (₹): ",
        minimum=0
    )
    return {
        "price_shock_threshold":
            price_shock_threshold,
        "portfolio_loss_threshold":
            portfolio_loss_threshold,
        "asset_volatility_threshold":
            asset_volatility_threshold,
        "medium_volatility":
            medium_volatility,
        "high_volatility":
            high_volatility,
        "critical_volatility":
            critical_volatility,
        "minimum_liquidity":
            minimum_liquidity,
        "rebalance_threshold":
            rebalance_threshold,
         "transaction_cost_rate":
            transaction_cost_rate,
        "max_transaction_cost":
            max_transaction_cost
    }

def validate_inputs(capital, assets, risk):
    errors = []
    current_total = sum(
        asset["current_weight"]
        for asset in assets.values()
    )
    target_total = sum(
        asset["target_weight"]
        for asset in assets.values()
    )
    if not np.isclose(current_total, 1.0, atol=0.001):
        errors.append(
            f"Current allocations must total 100%. "
            f"Current total = {current_total * 100:.2f}%"
        )
    if not np.isclose(target_total, 1.0, atol=0.001):
        errors.append(
            f"Target allocations must total 100%. "
            f"Target total = {target_total * 100:.2f}%"
        )
    for symbol, asset in assets.items():
        if asset["current_weight"] > asset["max_allocation"]:
            errors.append(
                f"{symbol}: current allocation exceeds "
                f"maximum allowed allocation."
            )
        if asset["target_weight"] > asset["max_allocation"]:

            errors.append(
                f"{symbol}: target allocation exceeds "
                f"maximum allowed allocation."
            )
    if not (
        risk["medium_volatility"]
        < risk["high_volatility"]
        < risk["critical_volatility"]
    ):
        errors.append(
            "Volatility thresholds must follow: "
            "MEDIUM < HIGH < CRITICAL."
        )
    print("\n")
    print("=" * 70)
    print("INPUT VALIDATION")
    print("=" * 70)
    if errors:
        print("\n❌ INPUT VALIDATION FAILED\n")
        for error in errors:
            print("•", error)
        return False
    print("\n✅ All inputs are valid.")
    return True

def calculate_portfolio_return(assets, returns):
    portfolio_return = 0
    for symbol, asset in assets.items():
        portfolio_return += (
            asset["current_weight"]
            * returns[symbol]
        )
    return portfolio_return

def calculate_portfolio_volatility(assets):
    weighted_variance = 0
    for asset in assets.values():
        weighted_variance += (
            asset["current_weight"] ** 2
            * asset["volatility"] ** 2
        )
    return np.sqrt(weighted_variance)

def calculate_portfolio_liquidity(assets):
    liquidity = 0
    for asset in assets.values():
        liquidity += (
            asset["current_weight"]
            * asset["liquidity"]
        )
    return liquidity

def generate_returns(assets):
    print("\n")
    print("-" * 70)
    print("MARKET RETURN INPUT")
    print("-" * 70)
    returns = {}
    print(
        "\nEnter today's price movement for each asset."
    )
    for symbol in assets:
        returns[symbol] = get_percentage(
            f"{symbol} daily return (%): "
        )
        direction = input(
            f"{symbol} direction (U = rise, D = drop): "
        ).strip().upper()
        if direction == "D":
            returns[symbol] *= -1
    return returns

def detect_price_shocks(
    assets,
    returns,
    threshold
):
    alerts = []
    for symbol in assets:
        daily_return = returns[symbol]
        if abs(daily_return) >= threshold:
            direction = (
                "DROP"
                if daily_return < 0
                else "RISE"
            )
            alerts.append({
                "type": "MARKET SHOCK",
                "asset": symbol,
                "severity": "HIGH",
                "message":
                    f"{symbol} experienced a "
                    f"{direction} of "
                    f"{abs(daily_return) * 100:.2f}%"
            })
    return alerts
def detect_asset_volatility(
    assets,
    threshold
):
    alerts = []
    for symbol, asset in assets.items():
        volatility = asset["volatility"]
        if volatility >= threshold:
            alerts.append({
                "type": "HIGH VOLATILITY",
                "asset": symbol,
                "severity": "MEDIUM",
                "message":
                    f"{symbol} volatility is "
                    f"{volatility * 100:.2f}%"
                               })
    return alerts

def detect_portfolio_loss(
    portfolio_return,
    threshold
):
    alerts = []
    if portfolio_return <= -threshold:
        alerts.append({
            "type": "PORTFOLIO LOSS",
            "asset": "PORTFOLIO",
            "severity": "CRITICAL",
            "message":
                f"Portfolio lost "
                f"{abs(portfolio_return) * 100:.2f}% today"
        })
    return alerts

def classify_volatility(
    volatility,
    risk
):
    if volatility >= risk["critical_volatility"]:
        return "VERY HIGH"
    elif volatility >= risk["high_volatility"]:
        return "HIGH"
    elif volatility >= risk["medium_volatility"]:
        return "MEDIUM"
    return "LOW"

def detect_portfolio_volatility(
    volatility,
    risk
):
    alerts = []
    level = classify_volatility(
        volatility,
        risk
    )
    if level == "VERY HIGH":
        alerts.append({
            "type": "PORTFOLIO VOLATILITY",
            "asset": "PORTFOLIO",
            "severity": "CRITICAL",
            "message":
                f"Portfolio volatility reached "
                f"{volatility * 100:.2f}%"
        })
    elif level == "HIGH":
        alerts.append({
            "type": "PORTFOLIO VOLATILITY",
            "asset": "PORTFOLIO",
            "severity": "HIGH",
            "message":
                f"Portfolio volatility reached "
                f"{volatility * 100:.2f}%"
        })
    elif level == "MEDIUM":
         alerts.append({
            "type": "PORTFOLIO VOLATILITY",
            "asset": "PORTFOLIO",
            "severity": "MEDIUM",
            "message":
                f"Portfolio volatility is elevated: "
                f"{volatility * 100:.2f}%"
        })
    return alerts

def check_liquidity(
    assets,
    minimum_liquidity
):
    alerts = []
    for symbol, asset in assets.items():
        if asset["liquidity"] < minimum_liquidity:
            alerts.append({
                "type": "LIQUIDITY BREACH",
                "asset": symbol,
                "severity": "HIGH",
                "message":
                    f"{symbol} liquidity score "
                    f"{asset['liquidity']:.1f} is below "
                    f"minimum required "
                    f"{minimum_liquidity:.1f}"
            })
    return alerts

def check_allocation_limits(assets):
    alerts = []
    for symbol, asset in assets.items():
        if (
            asset["current_weight"]
            > asset["max_allocation"]
        ):
            alerts.append({
                "type": "ALLOCATION BREACH",
                "asset": symbol,
                "severity": "HIGH",
                "message":
                    f"{symbol} current allocation "
                    f"exceeds maximum limit"
            })
    return alerts

def check_rebalancing(
    assets,
    capital,
    threshold
):
    trades = []
    for symbol, asset in assets.items():
        current = asset["current_weight"]
        target = asset["target_weight"]
        difference = target - current
        if abs(difference) < threshold:
            trades.append({

                "asset": symbol,

                "action": "NO REBALANCE",

                "difference": difference,

                "trade_value": 0
            })
        elif difference > 0:
            trade_value = (
                difference * capital
            )
            trades.append({
                "asset": symbol,
                "action": "BUY",
                "difference": difference,
                "trade_value": trade_value
            })
        else:
            trade_value = (
                abs(difference)
                * capital
            )
            trades.append({
                "asset": symbol,
                "action": "SELL",
                "difference": difference,
                "trade_value": trade_value
            })
    return trades

def calculate_transaction_cost(
    trades,
    transaction_cost_rate,
    maximum_cost
):
    total_trade_value = sum(
        trade["trade_value"]
        for trade in trades
    )
    estimated_cost = (
        total_trade_value
        * transaction_cost_rate
    )
    within_limit = (
        estimated_cost <= maximum_cost
    )
    return {
        "total_trade_value":
            total_trade_value,
        "estimated_cost":
            estimated_cost,
        "maximum_cost":
            maximum_cost,
        "within_limit":
            within_limit
    }

def determine_risk_level(alerts):
    severities = [
        alert["severity"]
        for alert in alerts
    ]
    if "CRITICAL" in severities:
        return "CRITICAL"
    elif "HIGH" in severities:
        return "HIGH"
    elif "MEDIUM" in severities:
        return "MEDIUM"
    return "LOW"

def generate_safeguard_decision(
    risk_level,
    alerts,
    transaction_cost
):
    critical = any(
        alert["severity"] == "CRITICAL"
        for alert in alerts
    )
    high = any(
        alert["severity"] == "HIGH"
        for alert in alerts
    )
    if critical:
        return {
            "action":
                "EMERGENCY REVIEW",
            "capital_deployment":
                "FROZEN",
            "rebalancing":
                "REQUIRED",
            "message":
                "Critical risk detected. "
                "Freeze new capital deployment "
                "and perform emergency portfolio review."
        }
    if high:
        if transaction_cost["within_limit"]:
            return {
                "action":
                    "REBALANCE",
                "capital_deployment":
                    "RESTRICTED",
                "rebalancing":
                    "REQUIRED",
                "message":
                    "High risk detected. "
                    "Cost-aware rebalancing is recommended."
            }
        else:
            return {
                "action":
                    "MONITOR",
                "capital_deployment":
                    "RESTRICTED",
                "rebalancing":
                    "DELAYED",
                "message":
                    "Risk detected, but transaction "
                    "cost exceeds the allowed limit."
            }
    if risk_level == "MEDIUM":
        return {
            "action":
                "MONITOR",
            "capital_deployment":
                "NORMAL",
            "rebalancing":
                "OPTIONAL",
            "message":
                "Moderate risk detected. "
                "Increase monitoring frequency."
        }
    return {
        "action":
            "HOLD",
        "capital_deployment":
            "NORMAL",
        "rebalancing":
            "NOT REQUIRED",
        "message":
            "Risk level is within normal limits."
    }

def display_results(
    capital,
    assets,
    returns,
    portfolio_return,
    portfolio_volatility,
    liquidity,
    alerts,
    trades,
    transaction_cost,
    decision,
    risk_level
):
    print("\n")
    print("=" * 70)
    print("              RISK MANAGEMENT REPORT")
    print("=" * 70)
    print(
        f"\nReport Time: {datetime.now()}"
    )
    print(
        f"Capital: ₹{capital:,.2f}"
    )
    print("\n")
    print("-" * 70)
    print("PORTFOLIO METRICS")
    print("-" * 70)
    print(
        f"Portfolio Return: "
        f"{portfolio_return * 100:.2f}%"
    )
    print(
        f"Portfolio Volatility: "
        f"{portfolio_volatility * 100:.2f}%"
    )
    print(
        f"Portfolio Liquidity: "
        f"{liquidity:.2f}/100"
    )
    print(
        f"Overall Risk Level: "
        f"{risk_level}"
    )
    print("\n")
    print("-" * 70)
    print("ASSET RISK")
    print("-" * 70)
    for symbol, asset in assets.items():
        print(
            f"\n{symbol}"
        )
        print(
            f"  Current Allocation: "
            f"{asset['current_weight'] * 100:.2f}%"
        )
        print(
            f"  Target Allocation: "
            f"{asset['target_weight'] * 100:.2f}%"
        )
        print(
            f"  Daily Return: "
            f"{returns[symbol] * 100:.2f}%"
        )
        print(
            f"  Volatility: "
            f"{asset['volatility'] * 100:.2f}%"
        )
        print(
            f"  Liquidity: "
            f"{asset['liquidity']:.1f}/100"
        )
    print("\n")
    print("-" * 70)
    print("RISK ALERTS")
    print("-" * 70)
    if not alerts:
        print(
            "\n✅ No risk threshold breaches detected."
        )
    else:
        for alert in alerts:
            print(
                f"\n[{alert['severity']}] "
                f"{alert['type']}"
            )
            print(
                f"Asset: {alert['asset']}"
            )
            print(
                f"Message: {alert['message']}"
            )
    print("\n")
    print("-" * 70)
    print("REBALANCING CHECK")
    print("-" * 70)
    for trade in trades:
        print(
            f"\n{trade['asset']}: "
            f"{trade['action']}"
        )
        if trade["trade_value"] > 0:
            print(
                f"Trade Value: "
                f"₹{trade['trade_value']:,.2f}"
            )
    print("\n")
    print("-" * 70)
    print("TRANSACTION COST")
    print("-" * 70)
    print(
        f"\nTotal Trade Value: "
        f"₹{transaction_cost['total_trade_value']:,.2f}"
    )
    print(
        f"Estimated Cost: "
        f"₹{transaction_cost['estimated_cost']:,.2f}"
    )
    print(
        f"Maximum Allowed: "
        f"₹{transaction_cost['maximum_cost']:,.2f}"
    )
    if transaction_cost["within_limit"]:
        print(
            "\n✅ Transaction cost is within limit."
             )
    else:
        print(
            "\n❌ Transaction cost exceeds limit."
        )
    print("\n")
    print("=" * 70)
    print("              AUTOMATED SAFEGUARD")
    print("=" * 70)
    print(
        f"\nACTION: "
        f"{decision['action']}"
    )
    print(
        f"Capital Deployment: "
        f"{decision['capital_deployment']}"
    )
    print(
        f"Rebalancing: "
        f"{decision['rebalancing']}"
    )
    print(
        f"\nRecommendation:"
            )
    print(
        decision["message"]
    )
def run_risk_management():
    capital, assets = get_portfolio_input()
    risk = get_risk_parameters()
    valid = validate_inputs(
        capital,
        assets,
        risk
    )
    if not valid:
        print(
            "\nPlease correct the input values "
            "and run the program again."
        )
        return
    returns = generate_returns(
        assets
    )
    portfolio_return = (
        calculate_portfolio_return(
            assets,
            returns
        )
    )
    portfolio_volatility = (
        calculate_portfolio_volatility(
            assets
        )
    )
    portfolio_liquidity = (
        calculate_portfolio_liquidity(
            assets
        )
    )
    alerts = []
    alerts.extend(
        detect_price_shocks(
            assets,
            returns,
            risk["price_shock_threshold"]
        )
    )
    alerts.extend(
        detect_asset_volatility(
            assets,
            risk["asset_volatility_threshold"]
        )
    )
    alerts.extend(
        detect_portfolio_loss(
            portfolio_return,
            risk["portfolio_loss_threshold"]
        )
    )
    alerts.extend(
        detect_portfolio_volatility(
            portfolio_volatility,
            risk
        )
    )
    alerts.extend(
        check_liquidity(
            assets,
            risk["minimum_liquidity"]
        )
    )
    alerts.extend(
        check_allocation_limits(
            assets
        )
    )
    risk_level = determine_risk_level(
        alerts
    )
    trades = check_rebalancing(
        assets,
        capital,
        risk["rebalance_threshold"]
    )
    transaction_cost = (
        calculate_transaction_cost(
            trades,
            risk["transaction_cost_rate"],
            risk["max_transaction_cost"]
        )
    )
    decision = generate_safeguard_decision(
        risk_level,
        alerts,
        transaction_cost
    )
    display_results(
        capital,
        assets,
        returns,
        portfolio_return,
        portfolio_volatility,
        portfolio_liquidity,
        alerts,
        trades,
        transaction_cost,
        decision,
        risk_level
    )
if __name__ == "__main__":
    run_risk_management()
