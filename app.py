import io
import os
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

from styles import CSS_STYLES
from ui_components import (
    apply_custom_css,
    render_top_navbar,
    render_welcome_header,
    render_kpi_card,
    render_insight_card,
    render_progress_bar,
    apply_plotly_theme,
    COLOR_PRIMARY_TEAL,
    COLOR_ACCENT_TEAL,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_AMBER,
    COLOR_BLUE,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BORDER,
)

DATA_FILE = "transactions.csv"
BUDGET_FILE = "budgets.csv"
GOALS_FILE = "goals.csv"

COLUMNS = ["ID", "Type", "Amount", "Category", "Date", "Time", "Description"]
BUDGET_COLUMNS = ["Category", "Limit"]
GOALS_COLUMNS = ["ID", "GoalName", "TargetAmount", "CurrentAmount", "CreatedDate"]

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Business", "Investment", "Interest/Dividends",
    "Rental Income", "Gift", "Other Income",
]
EXPENSE_CATEGORIES = [
    "Food & Dining", "Groceries", "Transportation", "Rent", "EMI/Loan",
    "Bills & Utilities", "Mobile/Internet Recharge", "Insurance", "Shopping",
    "Entertainment", "Health & Fitness", "Education", "Travel",
    "Festivals & Gifts", "Other Expense",
]

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()

# Navigation State Setup
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"


# ==========================================
# BUSINESS LOGIC & DATA STORAGE FUNCTIONS
# ==========================================

def format_inr(value) -> str:
    negative = value < 0
    value = abs(value)
    whole = int(value)
    decimal = round(value - whole, 2)
    decimal_str = f"{decimal:.2f}".split(".")[1]

    s = str(whole)
    if len(s) <= 3:
        grouped = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3

    result = f"{grouped}.{decimal_str}"
    return f"-₹{result}" if negative else f"₹{result}"


def format_inr_pdf(value) -> str:
    negative = value < 0
    value = abs(value)
    whole = int(value)
    decimal = round(value - whole, 2)
    decimal_str = f"{decimal:.2f}".split(".")[1]

    s = str(whole)
    if len(s) <= 3:
        grouped = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3

    result = f"Rs. {grouped}.{decimal_str}"
    return f"-{result}" if negative else result


def load_data() -> pd.DataFrame:
    try:
        if not os.path.exists(DATA_FILE):
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(DATA_FILE, index=False)
            return df

        df = pd.read_csv(DATA_FILE)
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)

        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
        df = df.dropna(subset=["Amount", "Date"])
        return df
    except Exception as e:
        st.error(f"Error loading transactions: {e}")
        return pd.DataFrame(columns=COLUMNS)


def save_data(df: pd.DataFrame) -> None:
    try:
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving transactions: {e}")


def add_transaction(t_type, amount, category, t_date, t_time, description):
    df = load_data()
    new_id = int(df["ID"].max()) + 1 if not df.empty else 1
    new_row = {
        "ID": new_id,
        "Type": t_type,
        "Amount": round(float(amount), 2),
        "Category": category,
        "Date": t_date,
        "Time": t_time,
        "Description": description,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    return new_id


def update_transaction(t_id, t_type, amount, category, t_date, t_time, description) -> bool:
    df = load_data()
    idx = df.index[df["ID"] == t_id]
    if len(idx) == 0:
        return False
    i = idx[0]
    df.loc[i, "Type"] = t_type
    df.loc[i, "Amount"] = round(float(amount), 2)
    df.loc[i, "Category"] = category
    df.loc[i, "Date"] = t_date
    df.loc[i, "Time"] = t_time
    df.loc[i, "Description"] = description
    save_data(df)
    return True


def delete_transactions(ids_to_delete):
    df = load_data()
    df = df[~df["ID"].isin(ids_to_delete)]
    save_data(df)


def load_budgets() -> pd.DataFrame:
    try:
        if not os.path.exists(BUDGET_FILE):
            df = pd.DataFrame(columns=BUDGET_COLUMNS)
            df.to_csv(BUDGET_FILE, index=False)
            return df
        df = pd.read_csv(BUDGET_FILE)
        if df.empty:
            return pd.DataFrame(columns=BUDGET_COLUMNS)
        df["Limit"] = pd.to_numeric(df["Limit"], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"Error loading budgets: {e}")
        return pd.DataFrame(columns=BUDGET_COLUMNS)


def save_budgets(df: pd.DataFrame) -> None:
    try:
        df.to_csv(BUDGET_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving budgets: {e}")


def set_budget(category: str, limit: float) -> None:
    df = load_budgets()
    if category in df["Category"].values:
        df.loc[df["Category"] == category, "Limit"] = round(float(limit), 2)
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"Category": category, "Limit": round(float(limit), 2)}])],
            ignore_index=True,
        )
    save_budgets(df)


def delete_budget(category: str) -> None:
    df = load_budgets()
    df = df[df["Category"] != category]
    save_budgets(df)


def load_goals() -> pd.DataFrame:
    try:
        if not os.path.exists(GOALS_FILE):
            df = pd.DataFrame(columns=GOALS_COLUMNS)
            df.to_csv(GOALS_FILE, index=False)
            return df
        df = pd.read_csv(GOALS_FILE)
        if df.empty:
            return pd.DataFrame(columns=GOALS_COLUMNS)
        df["TargetAmount"] = pd.to_numeric(df["TargetAmount"], errors="coerce").fillna(0)
        df["CurrentAmount"] = pd.to_numeric(df["CurrentAmount"], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"Error loading savings goals: {e}")
        return pd.DataFrame(columns=GOALS_COLUMNS)


def save_goals(df: pd.DataFrame) -> None:
    try:
        df.to_csv(GOALS_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving savings goals: {e}")


def add_goal(name: str, target: float, current: float) -> int:
    df = load_goals()
    new_id = int(df["ID"].max()) + 1 if not df.empty else 1
    row = {
        "ID": new_id,
        "GoalName": name,
        "TargetAmount": round(float(target), 2),
        "CurrentAmount": round(float(current), 2),
        "CreatedDate": date.today(),
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_goals(df)
    return new_id


def update_goal_amount(goal_id: int, new_amount: float) -> None:
    df = load_goals()
    df.loc[df["ID"] == goal_id, "CurrentAmount"] = round(float(new_amount), 2)
    save_goals(df)


def delete_goal(goal_id: int) -> None:
    df = load_goals()
    df = df[df["ID"] != goal_id]
    save_goals(df)


def compute_summary(df: pd.DataFrame):
    total_income = df.loc[df["Type"] == "Income", "Amount"].sum()
    total_expense = df.loc[df["Type"] == "Expense", "Amount"].sum()
    balance = total_income - total_expense
    savings = balance
    return total_income, total_expense, balance, savings


def avg_daily_spending(df: pd.DataFrame) -> float:
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        return 0.0
    days = (exp_df["Date"].max() - exp_df["Date"].min()).days + 1
    days = max(days, 1)
    return exp_df["Amount"].sum() / days


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["Income", "Expense"])
    dfm = df.copy()
    dfm["Month"] = pd.to_datetime(dfm["Date"]).dt.strftime("%Y-%m")
    monthly = dfm.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0)
    for col in ["Income", "Expense"]:
        if col not in monthly.columns:
            monthly[col] = 0
    return monthly.sort_index()


def generate_insights(df: pd.DataFrame) -> dict:
    messages = []
    result = {"highest_category": None, "lowest_category": None, "mom_change_pct": None, "messages": messages}

    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        messages.append("Not enough expense data yet to generate insights.")
        return result

    cat_sum = exp_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    highest_cat, lowest_cat = cat_sum.index[0], cat_sum.index[-1]
    result["highest_category"] = highest_cat
    result["lowest_category"] = lowest_cat
    messages.append(f"Highest spending category: {highest_cat} ({format_inr(cat_sum.iloc[0])}).")
    messages.append(f"Lowest spending category: {lowest_cat} ({format_inr(cat_sum.iloc[-1])}).")

    dfm = df.copy()
    dfm["Month"] = pd.to_datetime(dfm["Date"]).dt.to_period("M")
    months_sorted = sorted(dfm["Month"].unique())
    if len(months_sorted) >= 2:
        current_month, prev_month = months_sorted[-1], months_sorted[-2]
        cur_exp = dfm[(dfm["Month"] == current_month) & (dfm["Type"] == "Expense")]["Amount"].sum()
        prev_exp = dfm[(dfm["Month"] == prev_month) & (dfm["Type"] == "Expense")]["Amount"].sum()
        if prev_exp > 0:
            change_pct = ((cur_exp - prev_exp) / prev_exp) * 100
            result["mom_change_pct"] = change_pct
            if change_pct > 0:
                messages.append(f"Spending increased {change_pct:.1f}% vs. last month.")
            elif change_pct < 0:
                messages.append(f"Spending decreased {abs(change_pct):.1f}% vs. last month — nice work.")
            else:
                messages.append("Spending is unchanged from last month.")

    total_income, _, _, savings = compute_summary(df)
    if total_income > 0:
        savings_rate = (savings / total_income) * 100
        if savings_rate < 10:
            messages.append(f"Savings rate is {savings_rate:.1f}%. Aim for at least 20% of income saved.")
        else:
            messages.append(f"Savings rate is {savings_rate:.1f}% — solid progress.")

    return result


def pdf_safe(text) -> str:
    text = str(text)
    replacements = {
        "₹": "Rs. ",
        "—": "-",
        "–": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf_report(df: pd.DataFrame, budgets_df: pd.DataFrame, goals_df: pd.DataFrame) -> bytes:
    total_income, total_expense, balance, savings = compute_summary(df)
    insights = generate_insights(df)
    monthly = monthly_totals(df)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 10, "FinTrack AI - Financial Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(6)

    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Financial Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for label, val in [
        ("Total Income", format_inr_pdf(total_income)),
        ("Total Expenses", format_inr_pdf(total_expense)),
        ("Current Balance", format_inr_pdf(balance)),
        ("Total Savings", format_inr_pdf(savings)),
    ]:
        pdf.cell(95, 8, label)
        pdf.cell(95, 8, val, ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Monthly Summary", ln=True)
    if monthly.empty:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, "No transaction data available.", ln=True)
    else:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(60, 7, "Month", border=1)
        pdf.cell(60, 7, "Income", border=1)
        pdf.cell(60, 7, "Expense", border=1, ln=True)
        pdf.set_font("Helvetica", "", 10)
        for month, row in monthly.iterrows():
            pdf.cell(60, 7, pdf_safe(month), border=1)
            pdf.cell(60, 7, format_inr_pdf(row["Income"]), border=1)
            pdf.cell(60, 7, format_inr_pdf(row["Expense"]), border=1, ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Expense Category Analysis", ln=True)
    exp_df = df[df["Type"] == "Expense"]
    if exp_df.empty:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, "No expense data available.", ln=True)
    else:
        cat_sum = exp_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(90, 7, "Category", border=1)
        pdf.cell(90, 7, "Total Spent", border=1, ln=True)
        pdf.set_font("Helvetica", "", 10)
        for cat, amt in cat_sum.items():
            pdf.cell(90, 7, pdf_safe(cat), border=1)
            pdf.cell(90, 7, format_inr_pdf(amt), border=1, ln=True)
    pdf.ln(4)

    inc_df = df[df["Type"] == "Income"]
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Income Category Analysis", ln=True)
    if inc_df.empty:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, "No income data available.", ln=True)
    else:
        inc_cat_sum = inc_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(90, 7, "Category", border=1)
        pdf.cell(90, 7, "Total Received", border=1, ln=True)
        pdf.set_font("Helvetica", "", 10)
        for cat, amt in inc_cat_sum.items():
            pdf.cell(90, 7, pdf_safe(cat), border=1)
            pdf.cell(90, 7, format_inr_pdf(amt), border=1, ln=True)
    pdf.ln(4)

    if not budgets_df.empty:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, "Budget Overview", ln=True)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(63, 7, "Category", border=1)
        pdf.cell(63, 7, "Limit", border=1)
        pdf.cell(64, 7, "Spent", border=1, ln=True)
        pdf.set_font("Helvetica", "", 10)
        exp_by_cat = exp_df.groupby("Category")["Amount"].sum() if not exp_df.empty else pd.Series(dtype=float)
        for _, brow in budgets_df.iterrows():
            spent = exp_by_cat.get(brow["Category"], 0.0)
            pdf.cell(63, 7, pdf_safe(brow["Category"]), border=1)
            pdf.cell(63, 7, format_inr_pdf(brow["Limit"]), border=1)
            pdf.cell(64, 7, format_inr_pdf(spent), border=1, ln=True)
        pdf.ln(4)

    if not goals_df.empty:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, "Savings Goals", ln=True)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(60, 7, "Goal", border=1)
        pdf.cell(45, 7, "Target", border=1)
        pdf.cell(45, 7, "Saved", border=1)
        pdf.cell(40, 7, "Progress", border=1, ln=True)
        pdf.set_font("Helvetica", "", 10)
        for _, grow in goals_df.iterrows():
            pct = (grow["CurrentAmount"] / grow["TargetAmount"] * 100) if grow["TargetAmount"] > 0 else 0
            pdf.cell(60, 7, pdf_safe(grow["GoalName"]), border=1)
            pdf.cell(45, 7, format_inr_pdf(grow["TargetAmount"]), border=1)
            pdf.cell(45, 7, format_inr_pdf(grow["CurrentAmount"]), border=1)
            pdf.cell(40, 7, f"{pct:.1f}%", border=1, ln=True)
        pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Financial Insights", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for line in insights["messages"]:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 7, f"- {pdf_safe(line)}")

    return bytes(pdf.output())


def generate_excel_bytes(df: pd.DataFrame, budgets_df: pd.DataFrame, goals_df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        (df if not df.empty else pd.DataFrame(columns=COLUMNS)).to_excel(
            writer, index=False, sheet_name="Transactions"
        )
        monthly = monthly_totals(df)
        (monthly if not monthly.empty else pd.DataFrame(columns=["Income", "Expense"])).to_excel(
            writer, sheet_name="Monthly Summary"
        )
        exp_df = df[df["Type"] == "Expense"]
        if not exp_df.empty:
            cat_sum = exp_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            cat_sum.to_frame("Total Spent").to_excel(writer, sheet_name="Category Summary")
        if not budgets_df.empty:
            budgets_df.to_excel(writer, index=False, sheet_name="Budgets")
        if not goals_df.empty:
            goals_df.to_excel(writer, index=False, sheet_name="Savings Goals")
    return output.getvalue()


# Load All Data
df_all = load_data()
budgets_all = load_budgets()
goals_all = load_goals()

# Render Top Navbar
current_page = st.session_state.get("current_page", "Dashboard")
render_top_navbar(current_page)


# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if current_page == "Dashboard":
    render_welcome_header(
        "Executive Dashboard",
        "Real-time overview of cash flow, total savings, and spending patterns.",
        badge_text="Live Account"
    )

    total_income, total_expense, balance, savings = compute_summary(df_all)

    # Core Summary KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Income", format_inr(total_income), "All lifetime credits", delta="Income", delta_type="positive")
    with c2:
        render_kpi_card("Total Expenses", format_inr(total_expense), "All lifetime debits", delta="Expense", delta_type="negative")
    with c3:
        bal_delta = "Positive" if balance >= 0 else "Negative"
        bal_type = "positive" if balance >= 0 else "negative"
        render_kpi_card("Current Balance", format_inr(balance), "Net available capital", delta=bal_delta, delta_type=bal_type)
    with c4:
        render_kpi_card("Total Savings", format_inr(savings), "Net position", delta="Savings", delta_type="positive")

    if not df_all.empty:
        exp_df = df_all[df_all["Type"] == "Expense"]
        inc_df = df_all[df_all["Type"] == "Income"]
        highest_expense = exp_df["Amount"].max() if not exp_df.empty else 0.0
        highest_income = inc_df["Amount"].max() if not inc_df.empty else 0.0
        avg_daily = avg_daily_spending(df_all)
        total_txn = len(df_all)
    else:
        highest_expense = highest_income = avg_daily = 0.0
        total_txn = 0

    # Secondary Financial Metrics
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        render_kpi_card("Avg. Daily Spend", format_inr(avg_daily), "Per calendar day")
    with d2:
        render_kpi_card("Highest Expense", format_inr(highest_expense), "Single debit max")
    with d3:
        render_kpi_card("Highest Income", format_inr(highest_income), "Single credit max")
    with d4:
        render_kpi_card("Transactions", f"{total_txn}", "Total logged entries")

    st.markdown("<br>", unsafe_allow_html=True)

    if df_all.empty:
        st.info("No transactions logged yet. Navigate to **Transactions** to add your first record.")
    else:
        col_a, col_b = st.columns([1.4, 1])

        with col_a:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Cash Flow Trend</h3>", unsafe_allow_html=True)
            trend = df_all.groupby(["Date", "Type"])["Amount"].sum().reset_index()
            fig = px.line(
                trend, x="Date", y="Amount", color="Type", markers=True,
                color_discrete_map={"Income": COLOR_GREEN, "Expense": COLOR_RED},
            )
            fig.update_traces(line=dict(shape="spline", width=3))
            fig = apply_plotly_theme(fig)
            fig.update_layout(height=360)
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Expense Breakdown</h3>", unsafe_allow_html=True)
            exp_df = df_all[df_all["Type"] == "Expense"]
            if not exp_df.empty:
                cat_sum = exp_df.groupby("Category")["Amount"].sum().reset_index()
                fig2 = px.pie(
                    cat_sum, names="Category", values="Amount", hole=0.6,
                    color_discrete_sequence=[COLOR_ACCENT_TEAL, COLOR_PRIMARY_TEAL, COLOR_BLUE, COLOR_AMBER, COLOR_GREEN, "#38BDF8"]
                )
                fig2 = apply_plotly_theme(fig2)
                fig2.update_layout(height=360)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No expense entries logged yet.")

        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-top: 16px;'>Recent Transactions</h3>", unsafe_allow_html=True)
        recent = df_all.sort_values(by=["Date", "Time"], ascending=False).head(5)
        st.dataframe(recent, use_container_width=True, hide_index=True)


# ==========================================
# PAGE 2: ANALYTICS
# ==========================================
elif current_page == "Analytics":
    render_welcome_header(
        "Financial Analytics",
        "Deep visual analytics into spending trends, income streams, and savings velocity."
    )

    if df_all.empty:
        st.info("No transaction data recorded yet.")
    else:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Income vs Expense Trajectory</h3>", unsafe_allow_html=True)
        trend = df_all.groupby(["Date", "Type"])["Amount"].sum().reset_index()
        fig1 = px.line(
            trend, x="Date", y="Amount", color="Type", markers=True,
            color_discrete_map={"Income": COLOR_GREEN, "Expense": COLOR_RED},
        )
        fig1.update_traces(line=dict(shape="spline", width=3))
        fig1 = apply_plotly_theme(fig1)
        fig1.update_layout(height=380)
        st.plotly_chart(fig1, use_container_width=True)

        col_a, col_b = st.columns(2)
        exp_df = df_all[df_all["Type"] == "Expense"]
        inc_df = df_all[df_all["Type"] == "Income"]

        with col_a:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Expense Category Share</h3>", unsafe_allow_html=True)
            if not exp_df.empty:
                cat_sum = exp_df.groupby("Category")["Amount"].sum().reset_index()
                fig2 = px.pie(cat_sum, names="Category", values="Amount", hole=0.5)
                fig2 = apply_plotly_theme(fig2)
                fig2.update_layout(height=360)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No expenses recorded yet.")

        with col_b:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Income Source Share</h3>", unsafe_allow_html=True)
            if not inc_df.empty:
                inc_cat_sum = inc_df.groupby("Category")["Amount"].sum().reset_index()
                fig_inc = px.pie(inc_cat_sum, names="Category", values="Amount", hole=0.5)
                fig_inc.update_traces(marker=dict(colors=[COLOR_GREEN, "#4ADE80", "#86EFAC", COLOR_PRIMARY_TEAL, COLOR_ACCENT_TEAL]))
                fig_inc = apply_plotly_theme(fig_inc)
                fig_inc.update_layout(height=360)
                st.plotly_chart(fig_inc, use_container_width=True)
            else:
                st.info("No income recorded yet.")

        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Daily Spending Volatility</h3>", unsafe_allow_html=True)
        if not exp_df.empty:
            daily = exp_df.groupby("Date")["Amount"].sum().reset_index()
            fig3 = px.bar(daily, x="Date", y="Amount")
            fig3.update_traces(marker_color=COLOR_PRIMARY_TEAL, marker_line_color=COLOR_ACCENT_TEAL, marker_line_width=1)
            fig3 = apply_plotly_theme(fig3)
            fig3.update_layout(height=350)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No expenses recorded yet.")

        col_c, col_d = st.columns(2)
        monthly = monthly_totals(df_all)

        with col_c:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Monthly Expense Totals</h3>", unsafe_allow_html=True)
            if not monthly.empty:
                fig4 = px.bar(monthly.reset_index(), x="Month", y="Expense")
                fig4.update_traces(marker_color=COLOR_RED)
                fig4.update_xaxes(type="category")
                fig4 = apply_plotly_theme(fig4)
                fig4.update_layout(height=350)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No monthly data available yet.")

        with col_d:
            st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Monthly Income Totals</h3>", unsafe_allow_html=True)
            if not monthly.empty:
                fig5 = px.bar(monthly.reset_index(), x="Month", y="Income")
                fig5.update_traces(marker_color=COLOR_GREEN)
                fig5.update_xaxes(type="category")
                fig5 = apply_plotly_theme(fig5)
                fig5.update_layout(height=350)
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("No monthly data available yet.")

        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Cumulative Net Savings Growth</h3>", unsafe_allow_html=True)
        if not monthly.empty:
            savings_df = monthly.copy()
            savings_df["Net Savings"] = savings_df["Income"] - savings_df["Expense"]
            savings_df["Cumulative Savings"] = savings_df["Net Savings"].cumsum()
            fig6 = px.area(savings_df.reset_index(), x="Month", y="Cumulative Savings")
            fig6.update_traces(line_color=COLOR_ACCENT_TEAL, fillcolor="rgba(20, 184, 166, 0.2)")
            fig6.update_xaxes(type="category")
            fig6 = apply_plotly_theme(fig6)
            fig6.update_layout(height=350)
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("No monthly data available yet.")

        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Category Breakdown Summary</h3>", unsafe_allow_html=True)
        summary = df_all.groupby(["Type", "Category"])["Amount"].agg(["sum", "count"]).reset_index()
        summary.columns = ["Type", "Category", "Total Amount", "Transaction Count"]
        summary = summary.sort_values(by="Total Amount", ascending=False)
        st.dataframe(summary, use_container_width=True, hide_index=True)


# ==========================================
# PAGE 3: TRANSACTIONS
# ==========================================
elif current_page == "Transactions":
    render_welcome_header(
        "Transaction Ledger",
        "Filter, search, audit, record, edit, or remove financial entries."
    )

    if df_all.empty:
        st.info("No transactions logged yet. Use the form below to record your first entry.")
    else:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC;'>Search & Filter Controls</h3>", unsafe_allow_html=True)
        with st.container():
            f1, f2, f3, f4 = st.columns([1, 1, 1, 1.4])
            with f1:
                type_filter = st.multiselect("Transaction Type", ["Income", "Expense"], default=["Income", "Expense"])
            with f2:
                min_date, max_date = df_all["Date"].min(), df_all["Date"].max()
                date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
            with f3:
                all_cats = sorted(df_all["Category"].dropna().unique().tolist())
                cat_filter = st.multiselect("Category", all_cats, default=all_cats)
            with f4:
                search_term = st.text_input("Search Description", placeholder="e.g. Salary, Groceries...")

        filtered = df_all[df_all["Type"].isin(type_filter)]
        filtered = filtered[filtered["Category"].isin(cat_filter)]

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_d, end_d = date_range
            filtered = filtered[(filtered["Date"] >= start_d) & (filtered["Date"] <= end_d)]

        if search_term:
            filtered = filtered[
                filtered["Description"].astype(str).str.contains(search_term, case=False, na=False)
            ]

        filtered = filtered.sort_values(by=["Date", "Time"], ascending=False)

        st.markdown(f"<div style='margin: 12px 0; color: #94A3B8; font-weight: 600;'>Showing <b>{len(filtered)}</b> transaction(s)</div>", unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.markdown("<hr style='border-color: #2F3742; margin: 28px 0;'>", unsafe_allow_html=True)

    # Sub-tabs for Add / Edit / Delete Transactions
    tab_add, tab_edit, tab_delete = st.tabs(["➕ Add Transaction", "✏️ Edit Transaction", "🗑️ Delete Transactions"])

    with tab_add:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Record New Entry</h3>", unsafe_allow_html=True)
        with st.form("add_transaction_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                t_type = st.radio("Type", ["Income", "Expense"], horizontal=True)
                amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
                category_list = INCOME_CATEGORIES if t_type == "Income" else EXPENSE_CATEGORIES
                category = st.selectbox("Category", category_list)
            with col2:
                t_date = st.date_input("Date", value=date.today())
                t_time = st.time_input("Time", value=datetime.now().time().replace(microsecond=0))
                description = st.text_area("Description", placeholder="e.g. Monthly salary payout", height=95)

            submitted = st.form_submit_button("Save Transaction", use_container_width=True)

            if submitted:
                if amount <= 0:
                    st.error("Please enter an amount greater than 0.")
                else:
                    try:
                        new_id = add_transaction(t_type, amount, category, t_date, t_time, description)
                        st.success(f"{t_type} of {format_inr(amount)} recorded successfully! (ID #{new_id})")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not save transaction: {e}")

    with tab_edit:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Modify Entry</h3>", unsafe_allow_html=True)
        if df_all.empty:
            st.info("No transactions available to edit.")
        else:
            edit_id = st.selectbox(
                "Select Transaction ID to Edit",
                options=[None] + df_all["ID"].tolist(),
                format_func=lambda x: "— choose transaction —" if x is None else f"ID #{x}",
                key="edit_select",
            )
            if edit_id is not None:
                row = df_all[df_all["ID"] == edit_id].iloc[0]
                with st.form("edit_transaction_form"):
                    e_type = st.radio("Type", ["Income", "Expense"], index=0 if row["Type"] == "Income" else 1, horizontal=True)
                    e_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, value=float(row["Amount"]), format="%.2f")
                    e_cat_list = INCOME_CATEGORIES if e_type == "Income" else EXPENSE_CATEGORIES
                    e_cat_default = row["Category"] if row["Category"] in e_cat_list else e_cat_list[0]
                    e_category = st.selectbox("Category", e_cat_list, index=e_cat_list.index(e_cat_default))
                    e_date = st.date_input("Date", value=row["Date"])
                    e_description = st.text_area("Description", value=str(row.get("Description", "")))
                    save_edit = st.form_submit_button("Update Transaction", use_container_width=True)

                    if save_edit:
                        if e_amount <= 0:
                            st.error("Amount must be greater than 0.")
                        else:
                            try:
                                ok = update_transaction(
                                    edit_id, e_type, e_amount, e_category, e_date,
                                    row.get("Time", "00:00:00"), e_description,
                                )
                                if ok:
                                    st.success(f"Transaction #{edit_id} updated successfully.")
                                    st.rerun()
                                else:
                                    st.error("Transaction not found.")
                            except Exception as e:
                                st.error(f"Could not update transaction: {e}")

    with tab_delete:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Remove Entry</h3>", unsafe_allow_html=True)
        if df_all.empty:
            st.info("No transactions available to delete.")
        else:
            ids_to_delete = st.multiselect(
                "Select Transaction ID(s) to Delete",
                options=df_all["ID"].tolist(),
            )
            if st.button("Delete Selected Transactions", use_container_width=True):
                if ids_to_delete:
                    try:
                        delete_transactions(ids_to_delete)
                        st.success(f"Deleted {len(ids_to_delete)} transaction(s).")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not delete transactions: {e}")
                else:
                    st.warning("Select at least one transaction to delete.")


# ==========================================
# PAGE 4: AI INSIGHTS
# ==========================================
elif current_page == "AI Insights":
    render_welcome_header(
        "AI Financial Intelligence",
        "Automated intelligence recommendations based on your spending habits and income patterns.",
        badge_text="AI Engine Active"
    )

    insights = generate_insights(df_all)
    total_inc, total_exp, balance, savings = compute_summary(df_all)
    savings_rate = (savings / total_inc * 100) if total_inc > 0 else 0.0

    # Insight Overview Cards
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        sr_type = "positive" if savings_rate >= 20 else ("warning" if savings_rate >= 10 else "negative")
        render_kpi_card("Savings Rate", f"{savings_rate:.1f}%", "Target: >= 20%", delta="Rate", delta_type=sr_type)
    with i2:
        high_cat = insights.get("highest_category") or "N/A"
        render_kpi_card("Top Spend Area", str(high_cat), "Highest category outflow")
    with i3:
        low_cat = insights.get("lowest_category") or "N/A"
        render_kpi_card("Lowest Spend Area", str(low_cat), "Minimum category outflow")
    with i4:
        mom_change = insights.get("mom_change_pct")
        mom_text = f"{mom_change:+.1f}%" if mom_change is not None else "N/A"
        mom_type = "negative" if (mom_change and mom_change > 0) else "positive"
        render_kpi_card("MoM Expense Δ", mom_text, "Month over month change", delta="MoM", delta_type=mom_type)

    st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-top: 24px;'>Executive Recommendations</h3>", unsafe_allow_html=True)

    if not insights["messages"]:
        render_insight_card("Data Collection In Progress", "Log additional transactions to enable automated financial intelligence analysis.", icon="ℹ️")
    else:
        for idx, msg in enumerate(insights["messages"]):
            icon = "⚡" if "Highest" in msg else ("💡" if "Savings" in msg else "📈")
            render_insight_card(f"Insight #{idx + 1}", msg, icon=icon)


# ==========================================
# PAGE 5: SETTINGS
# ==========================================
elif current_page == "Settings":
    render_welcome_header(
        "Platform Settings & Management",
        "Configure monthly category budgets, manage long-term savings goals, and download financial reports."
    )

    tab_budget, tab_goals, tab_export = st.tabs(["🎯 Budget Planner", "🏆 Savings Goals", "📄 Data Export & Reports"])

    # --- BUDGET PLANNER ---
    with tab_budget:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Monthly Budget Limits</h3>", unsafe_allow_html=True)
        with st.form("set_budget_form"):
            b1, b2 = st.columns(2)
            with b1:
                budget_category = st.selectbox("Category", ["Overall (All Expenses)"] + EXPENSE_CATEGORIES)
            with b2:
                budget_limit = st.number_input("Monthly Limit (₹)", min_value=0.0, step=10.0, format="%.2f")
            set_submitted = st.form_submit_button("Save Budget Limit", use_container_width=True)

            if set_submitted:
                if budget_limit <= 0:
                    st.error("Please enter a limit greater than 0.")
                else:
                    try:
                        set_budget(budget_category, budget_limit)
                        st.success(f"Budget for '{budget_category}' set to {format_inr(budget_limit)}.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not save budget: {e}")

        st.markdown("<hr style='border-color: #2F3742; margin: 24px 0;'>", unsafe_allow_html=True)
        budgets_all = load_budgets()

        if budgets_all.empty:
            st.info("No category budgets set yet. Use the form above to define your limits.")
        else:
            this_month = date.today().strftime("%Y-%m")
            exp_df = df_all[df_all["Type"] == "Expense"].copy()
            if not exp_df.empty:
                exp_df["Month"] = pd.to_datetime(exp_df["Date"]).dt.strftime("%Y-%m")
                exp_this_month = exp_df[exp_df["Month"] == this_month]
            else:
                exp_this_month = exp_df

            for _, brow in budgets_all.iterrows():
                category, limit = brow["Category"], brow["Limit"]
                if category == "Overall (All Expenses)":
                    spent = exp_this_month["Amount"].sum() if not exp_this_month.empty else 0.0
                else:
                    spent = (
                        exp_this_month.loc[exp_this_month["Category"] == category, "Amount"].sum()
                        if not exp_this_month.empty else 0.0
                    )

                pct_used = min((spent / limit) * 100, 100) if limit > 0 else 0
                remaining = limit - spent
                bar_color = COLOR_RED if spent > limit else (COLOR_AMBER if pct_used >= 80 else COLOR_GREEN)

                col_info, col_delete = st.columns([5, 1])
                with col_info:
                    status_msg = "⚠️ Budget Exceeded!" if spent > limit else f"OK ({pct_used:.1f}% used)"
                    st.markdown(
                        f"""
                        <div class="fin-card">
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">
                                <span>{category}</span>
                                <span style="color: {bar_color};">{status_msg}</span>
                            </div>
                            <div class="fin-card-sub" style="margin-top: 4px;">Limit: {format_inr(limit)} | Spent: {format_inr(spent)} | Remaining: {format_inr(remaining)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    render_progress_bar(pct_used, color=bar_color)
                with col_delete:
                    st.write("")
                    if st.button("Remove", key=f"del_budget_{category}"):
                        delete_budget(category)
                        st.rerun()

    # --- SAVINGS GOALS ---
    with tab_goals:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Savings Target Tracking</h3>", unsafe_allow_html=True)
        with st.form("add_goal_form", clear_on_submit=True):
            g1, g2, g3 = st.columns(3)
            with g1:
                goal_name = st.text_input("Goal Name", placeholder="e.g. Emergency Reserve")
            with g2:
                goal_target = st.number_input("Target Amount (₹)", min_value=0.0, step=50.0, format="%.2f")
            with g3:
                goal_current = st.number_input("Already Saved (₹)", min_value=0.0, step=10.0, format="%.2f")
            goal_submitted = st.form_submit_button("Create Savings Goal", use_container_width=True)

            if goal_submitted:
                if not goal_name.strip():
                    st.error("Please enter a valid goal name.")
                elif goal_target <= 0:
                    st.error("Target amount must be greater than 0.")
                else:
                    try:
                        add_goal(goal_name.strip(), goal_target, goal_current)
                        st.success(f"Savings goal '{goal_name}' created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not create goal: {e}")

        st.markdown("<hr style='border-color: #2F3742; margin: 24px 0;'>", unsafe_allow_html=True)
        goals_all = load_goals()

        if goals_all.empty:
            st.info("No savings goals configured yet.")
        else:
            for _, grow in goals_all.iterrows():
                goal_id = int(grow["ID"])
                target, current = grow["TargetAmount"], grow["CurrentAmount"]
                pct = min((current / target) * 100, 100) if target > 0 else 0
                remaining = max(target - current, 0)

                col_info, col_update, col_delete = st.columns([4, 2, 1])
                with col_info:
                    st.markdown(
                        f"""
                        <div class="fin-card">
                            <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">{grow['GoalName']}</div>
                            <div class="fin-card-sub" style="margin-top: 4px;">Target: {format_inr(target)} | Saved: {format_inr(current)} | Remaining: {format_inr(remaining)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    render_progress_bar(pct, color=COLOR_ACCENT_TEAL, label="Target Progress")
                with col_update:
                    new_amount = st.number_input(
                        "Update saved (₹)", min_value=0.0, value=float(current), step=10.0, format="%.2f", key=f"goal_update_{goal_id}"
                    )
                    if st.button("Update Saved", key=f"goal_btn_{goal_id}"):
                        update_goal_amount(goal_id, new_amount)
                        st.rerun()
                with col_delete:
                    st.write("")
                    st.write("")
                    if st.button("Remove Goal", key=f"goal_del_{goal_id}"):
                        delete_goal(goal_id)
                        st.rerun()

    # --- DATA EXPORT & REPORTS ---
    with tab_export:
        st.markdown("<h3 style='font-size: 1.1rem; color: #F8FAFC; margin-bottom: 16px;'>Export Financial Statements</h3>", unsafe_allow_html=True)
        if df_all.empty:
            st.info("No transaction data available to export.")
        else:
            st.dataframe(df_all, use_container_width=True, hide_index=True)

            e1, e2, e3 = st.columns(3)

            with e1:
                csv_data = df_all.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export Raw CSV",
                    data=csv_data,
                    file_name=f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with e2:
                try:
                    excel_data = generate_excel_bytes(df_all, budgets_all, goals_all)
                    st.download_button(
                        label="📊 Export Excel Workbook (.xlsx)",
                        data=excel_data,
                        file_name=f"finance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Could not generate Excel file: {e}")

            with e3:
                try:
                    pdf_bytes = generate_pdf_report(df_all, budgets_all, goals_all)
                    st.download_button(
                        label="📄 Export Official PDF Report",
                        data=pdf_bytes,
                        file_name=f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Could not generate PDF report: {e}")