import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import os

    import matplotlib.pyplot as plt
    import polars as pl
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("BLS_API_KEY")

    if not api_key:
        raise ValueError("BLS_API_KEY not found in environment variables or .env file.")
    return api_key, json, pl, plt, requests


@app.cell
def _(api_key, json, requests):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": ["CUSR0000SA0", "CUSR0000SA0L1E", "CES0500000003"],
        "startyear": "2016",
        "endyear": "2026",
        "registrationKey": api_key,
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    json_data = response.json()

    rows = []
    for series in json_data.get("Results", {}).get("series", []):
        series_id = series["seriesID"]
        for item in series["data"]:
            rows.append(
                {
                    "series_id": series_id,
                    "year": item["year"],
                    "period": item["period"],
                    "value": item["value"],
                }
            )
    return (rows,)


@app.cell
def _(pl, rows):
    df = (
        pl.DataFrame(rows)
        .with_columns(
            pl.col("period").str.slice(1).cast(pl.Int32).alias("month"),
            pl.col("year").cast(pl.Int32).alias("year_int"),
            pl.when(pl.col("value") == "-")
            .then(None)
            .otherwise(pl.col("value"))
            .cast(pl.Float64)
            .alias("value"),
        )
        .with_columns(pl.date(pl.col("year_int"), pl.col("month"), 1).alias("date"))
        .select(["date", "series_id", "value"])
        .pivot(on="series_id", index="date", values="value")
        .rename(
            {
                "CUSR0000SA0": "cpi",
                "CUSR0000SA0L1E": "core_cpi",
                "CES0500000003": "wage",
            }
        )
        .sort("date")
    )
    return (df,)


@app.cell
def _(df, pl):
    df_inflation = df.with_columns(
        headline_inflation=100 * (pl.col("cpi") / pl.col("cpi").shift(12) - 1),
        core_inflation=100 * (pl.col("core_cpi") / pl.col("core_cpi").shift(12) - 1),
    )
    return (df_inflation,)


@app.cell
def _(df_inflation, pl):
    import datetime

    target_date = datetime.date(2025, 9, 1)

    base_sept = (
        df_inflation.filter(pl.col("date") == target_date)
        .select(["wage", "cpi"])
        .row(0, named=True)
    )
    base_wage = base_sept["wage"]
    base_cpi = base_sept["cpi"]

    df_since_sept = df_inflation.filter(pl.col("date") >= target_date).with_columns(
        wage_change=100 * (pl.col("wage") / base_wage - 1),
        price_change=100 * (pl.col("cpi") / base_cpi - 1),
    )
    return (df_since_sept,)


@app.cell
def _(df_inflation, df_since_sept, pl):
    # Get latest available row for overall inflation/wages
    latest_row = df_inflation.tail(1).row(0, named=True)

    # Find peak headline inflation and when it occurred
    peak_row = df_inflation.filter(
        pl.col("headline_inflation") == df_inflation["headline_inflation"].max()
    ).row(0, named=True)

    # Latest changes since Sept 2025
    latest_since_sept = df_since_sept.tail(1).row(0, named=True)

    print("=== WORKSHEET ANSWERS ===")
    print(f"1. Latest Date in Dataset: {latest_row['date']}")
    print(f"2. Latest Headline Inflation: {latest_row['headline_inflation']:.2f}%")
    print(f"3. Latest Core Inflation: {latest_row['core_inflation']:.2f}%")
    print(
        f"4. Peak Headline Inflation: {peak_row['headline_inflation']:.2f}% (in {peak_row['date']})"
    )
    print(f"5. Since Sept 2025 (Latest month: {latest_since_sept['date']}):")
    print(f"   - Prices are up: {latest_since_sept['price_change']:.2f}%")
    print(f"   - Wages are up: {latest_since_sept['wage_change']:.2f}%")


@app.cell
def _(df_inflation, pl, plt):
    # Filter data from 2017-01-01 onwards to match worksheet guidelines
    start_date = datetime.date(2017, 1, 1)
    plot_df = df_inflation.filter(pl.col("date") >= start_date)

    dates = plot_df["date"].to_numpy()
    headline = plot_df["headline_inflation"].to_numpy()
    core = plot_df["core_inflation"].to_numpy()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, headline, label="Headline Inflation", color="#2b5c8f", linewidth=2)
    ax.plot(
        dates,
        core,
        label="Core Inflation",
        color="#d95f02",
        linewidth=2,
        linestyle="--",
    )

    # Styling the chart
    ax.set_title(
        "Year-over-Year Inflation Trends (BLS Data)", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Inflation Rate (%)", fontsize=11)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.show()

    return ax, core, dates, fig, headline, plot_df, start_date


if __name__ == "__main__":
    app.run()
