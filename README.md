# BLS Wage & Price Dynamics Analysis

[![Live Report](https://img.shields.io/badge/Live_Report-GitHub_Pages-2ea44f?style=flat-square&logo=github)](https://tariq-k-dev.github.io/bls-wage-price-dynamics)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![uv](https://img.shields.io/badge/managed_by-uv-261230?style=flat-square)](https://github.com/astral-sh/uv)
[![marimo](https://img.shields.io/badge/built_with-marimo-1B1B1F?style=flat-square)](https://marimo.io/)

An interactive, reproducible economic analysis investigating **US Headline vs. Core CPI inflation** relative to **Average Hourly Earnings**. Inspired by Justin Wolfers' *Platypus Economics* worksheet, this project uses modern Python tools to evaluate purchasing power trends across custom baselines.

🌐 **Live Interactive Report:** [https://tariq-k-dev.github.io/bls-wage-price-dynamics](https://tariq-k-dev.github.io/bls-wage-price-dynamics)

---

## 📊 Overview

This report analyzes Bureau of Labor Statistics (BLS) time series to answer core questions on wage dynamics and price growth:
- **Headline CPI (`CUSR0000SA0`)**: All urban consumers, seasonally adjusted.
- **Core CPI (`CUSR0000SA0L1E`)**: All items less food and energy.
- **Average Hourly Earnings (`CES0500000003`)**: Total private sector hourly earnings.

The pipeline pulls fresh data via the BLS API v2, transforms and pivots time-series frames using **Polars**, and builds reactive visual summaries inside **marimo**.

---

## 🛠️ Tech Stack & Dependencies

- **Package & Virtual Environment Manager:** [`uv`](https://github.com/astral-sh/uv)
- **Data Processing:** [`polars`](https://pola.rs/)
- **Reactive Notebook / HTML Export:** [`marimo`](https://marimo.io/)
- **Visualization:** `matplotlib`
- **Configuration:** `python-dotenv`

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
Ensure you have `uv` installed on your system:
```bash
# Install uv if needed
pip install uv
```
