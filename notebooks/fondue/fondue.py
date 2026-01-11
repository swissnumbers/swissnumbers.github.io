import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("white")
sns.set_context("talk")

# 1) Load the CSV robustly
fn = "multiTimeline.csv"
df_raw = pd.read_csv(fn, skiprows=2)

# assume first column is date, next two are the two terms (Fondue, Raclette)
date_col = df_raw.columns[0]
term_cols = list(df_raw.columns[1:3])

# normalize names
df = df_raw[[date_col] + term_cols].copy()
df.columns = ["date", "Fondue", "Raclette"]
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["Fondue"] = pd.to_numeric(df["Fondue"], errors="coerce")
df["Raclette"] = pd.to_numeric(df["Raclette"], errors="coerce")
df = df.dropna(subset=["date"]).set_index("date").sort_index()

# small epsilon to avoid log(0)
eps = 1e-6

# 2) Time series visual (vibrant, readable)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

colors = {"Fondue": "#6A3D9A", "Raclette": "#FF7F00"}  # purple / orange

fig, ax = plt.subplots(figsize=(14,6))
ax.fill_between(df.index, df["Fondue"], color=colors["Fondue"], alpha=0.18)
ax.fill_between(df.index, df["Raclette"], color=colors["Raclette"], alpha=0.18)
ax.plot(df.index, df["Fondue"], color=colors["Fondue"], lw=2.6, label="Fondue", marker='o', markersize=4)
ax.plot(df.index, df["Raclette"], color=colors["Raclette"], lw=2.6, label="Raclette", marker='o', markersize=4)

# highlight latest values
last = df.iloc[-1]
ax.scatter(df.index[-1], last["Fondue"], color=colors["Fondue"], s=120, edgecolor='w', zorder=5)
ax.scatter(df.index[-1], last["Raclette"], color=colors["Raclette"], s=120, edgecolor='w', zorder=5)
ax.text(df.index[-1], last["Fondue"], f" {last['Fondue']:.0f}", va='center', fontsize=12, color=colors["Fondue"])
ax.text(df.index[-1], last["Raclette"], f" {last['Raclette']:.0f}", va='center', fontsize=12, color=colors["Raclette"])

ax.set_title("Google Search Interest over Time — Fondue vs Raclette", weight='bold', fontsize=18)
ax.set_ylabel("Search Interest (normalized)")
ax.legend(frameon=False, fontsize=13, loc='upper left')
ax.grid(alpha=0.12)
ax.set_xlim(df.index.min(), df.index.max())

# nice x ticks
if (df.index[-1] - df.index[0]).days > 365 * 2:
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
else:
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=30)

plt.tight_layout()

# 3) Yearly peak and total ratio analysis
# Extract year from index
df['year'] = df.index.year

# Group by year and compute peak (max) and total (sum) for each term
yearly_stats = df.groupby('year').agg({
    'Fondue': ['max', 'sum'],
    'Raclette': ['max', 'sum']
}).round(2)

# Flatten column names
yearly_stats.columns = ['fondue_peak', 'fondue_total', 'raclette_peak', 'raclette_total']

# Calculate ratios (Fondue / Raclette)
yearly_stats['ratio_peaks'] = yearly_stats['fondue_peak'] / (yearly_stats['raclette_peak'] + eps)
yearly_stats['ratio_totals'] = yearly_stats['fondue_total'] / (yearly_stats['raclette_total'] + eps)

# Create the ratio plot
fig, ax = plt.subplots(figsize=(14, 6))

years = yearly_stats.index.astype(str)
x_pos = np.arange(len(years))
width = 0.35

# Plot bars for peaks and totals
bars1 = ax.bar(x_pos - width/2, yearly_stats['ratio_peaks'], width, label='Peak Ratio (Fondue/Raclette)', 
               color="#6A3D9A", alpha=0.8)
bars2 = ax.bar(x_pos + width/2, yearly_stats['ratio_totals'], width, label='Total Ratio (Fondue/Raclette)', 
               color="#FF7F00", alpha=0.8)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)

# Horizontal line at ratio = 1 (equal interest)
ax.axhline(y=1, color='#444444', linestyle='--', lw=1, alpha=0.6, label='Equal interest (ratio=1)')

ax.set_xlabel('Year', fontsize=12, weight='bold')
ax.set_ylabel('Ratio (Fondue / Raclette)', fontsize=12, weight='bold')
ax.set_title('Yearly Peak vs Total Interest Ratios — Fondue/Raclette', weight='bold', fontsize=18)
ax.set_xticks(x_pos)
ax.set_xticklabels(years, rotation=45)
ax.legend(frameon=False, fontsize=11, loc='upper right')
ax.grid(alpha=0.12, axis='y')

plt.tight_layout()

# Save high-resolution PNGs for sharing (standalone)
fig1_path = "trend.png"
fig2_path = "ratio.png"
# re-save the two open figures: first is ratio figure currently, we need to re-create the first for saving as well
# recreate first figure for saving to ensure both are saved
fig_a, ax_a = plt.subplots(figsize=(14,6))
ax_a.fill_between(df.index, df["Fondue"], color=colors["Fondue"], alpha=0.18)
ax_a.fill_between(df.index, df["Raclette"], color=colors["Raclette"], alpha=0.18)
ax_a.plot(df.index, df["Fondue"], color=colors["Fondue"], lw=2.6, label="Fondue", marker='o', markersize=4)
ax_a.plot(df.index, df["Raclette"], color=colors["Raclette"], lw=2.6, label="Raclette", marker='o', markersize=4)
ax_a.set_title("Google Search Interest over Time — Fondue vs Raclette", weight='bold', fontsize=18)
ax_a.set_ylabel("Search Interest (normalized)")
ax_a.legend(frameon=False, fontsize=13, loc='upper left')
ax_a.grid(alpha=0.12)
if (df.index[-1] - df.index[0]).days > 365 * 2:
    ax_a.xaxis.set_major_locator(mdates.YearLocator())
    ax_a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
else:
    ax_a.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax_a.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=30)
plt.tight_layout()
fig_a.savefig(fig1_path, dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(fig2_path, dpi=300, bbox_inches="tight", facecolor="white")

print(f"Saved visuals: {fig1_path}, {fig2_path}")