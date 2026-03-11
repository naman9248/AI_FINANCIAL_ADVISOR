import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def plot_advised_financial_overview(user_data, analysis_data):
    expenses = user_data["expenses"]
    savings = analysis_data["savings"]
    emergency_fund_monthly = analysis_data["emergency_fund_monthly"]
    
    investment_allocation = analysis_data["recommended_investment_allocation"]
    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs = investment_allocation.get("ETFs / Balanced Funds", 0)
    risk_free = investment_allocation.get("Debt Mutual Funds / Bonds", 0)
    
    total_investments = high_interest + stocks + etfs + risk_free
    remaining_savings = max(0, savings - (emergency_fund_monthly + total_investments))
    
    labels = [
        "Expenses", 
        "Emergency Fund", 
        "High-Interest/RD",
        "Stocks/Equity",
        "ETFs/Balanced",
        "Debt/Bonds",
        "Unallocated Savings"
    ]
    
    values = [
        expenses,
        emergency_fund_monthly,
        high_interest,
        stocks,
        etfs,
        risk_free,
        remaining_savings
    ]
    
    # Filter out 0 values for cleaner plots
    filtered_data = [(l, v) for l, v in zip(labels, values) if v > 0]
    labels_filtered = [item[0] for item in filtered_data]
    values_filtered = [item[1] for item in filtered_data]

    colors = sns.color_palette("pastel", len(values_filtered))

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#F9FAFB")
    
    # Pie Chart
    wedges, texts, autotexts = ax[0].pie(
        values_filtered, 
        labels=labels_filtered, 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=140,
        textprops=dict(color="w") # For visibility if needed, or default
    )
    for text in texts:
        text.set_color("#222222")
    for autotext in autotexts:
        autotext.set_color("#222222")
        autotext.set_fontsize(9)
        
    ax[0].set_title("Savings & Investment Distribution", pad=35, fontweight="bold", fontsize=11, color="#222222")

    # Bar Chart
    sns.set_style("whitegrid")
    sns.barplot(x=labels_filtered, y=values_filtered, ax=ax[1], palette=colors)
    ax[1].set_facecolor("#FFFFFF")
    ax[1].grid(axis="y", linestyle="--", alpha=0.5)
    ax[1].set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax[1].tick_params(axis="x", rotation=90, labelsize=9)
    ax[1].set_title("Component-wise Financial Impact", pad=35, fontweight="bold", fontsize=11, color="#222222")

    for i, value in enumerate(values_filtered):
        ax[1].text(i, value + (max(values_filtered)*0.01), f"₹{value:,.0f}", ha='center', va='bottom', fontsize=9, color="#222222")

    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.95])
    plt.subplots_adjust(wspace=0.4)

    return fig

