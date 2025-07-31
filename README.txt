# 📈 Inflation vs Investment Plotter

A Python CLI tool to visualize how **inflation erodes purchasing power** over time and how **investment growth** competes against it, considering monthly withdrawals.

This tool generates an interactive **Plotly** graph showing:
- The decreasing value of a fixed amount `X` over `T` years with three inflation rates (`h1`, `h2`, `h3`).
- The growth of an investment `K` over `T` years at return rate `P%` per annum, while withdrawing `W` every month.

---

## 🔧 Requirements

- Python 3.7+
- Plotly

Install dependencies:

```bash
pip install plotly
