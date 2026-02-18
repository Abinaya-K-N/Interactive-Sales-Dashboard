import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os

# Create visualizations folder
if not os.path.exists("visualizations"):
    os.makedirs("visualizations")

# ---------------------------
# LOAD DATA WITH ERROR HANDLING
# ---------------------------

def load_data(file):
    try:
        df = pd.read_csv(file)
        print("Data loaded successfully")
        return df
    except FileNotFoundError:
        print("Error: File not found")
        return None

df = load_data("sales_data.csv")

if df is None:
    exit()

# ---------------------------
# BASIC CLEANING
# ---------------------------

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month

# ---------------------------
# SET STYLE
# ---------------------------

sns.set_theme(style="darkgrid", palette="Set2")

# ---------------------------
# 1. BOX PLOT
# ---------------------------

plt.figure(figsize=(8,6))
sns.boxplot(x='Region', y='Total_Sales', data=df)
plt.title("Sales Distribution by Region")
plt.savefig("visualizations/boxplot.png")
plt.show()

# ---------------------------
# 2. VIOLIN PLOT
# ---------------------------

plt.figure(figsize=(8,6))
sns.violinplot(x='Region', y='Total_Sales', data=df)
plt.title("Sales Density by Region")
plt.savefig("visualizations/violinplot.png")
plt.show()

# ---------------------------
# 3. HEATMAP
# ---------------------------

corr = df[['Total_Sales','Quantity']].corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("visualizations/heatmap.png")
plt.show()

# ---------------------------
# 4. SUBPLOTS DASHBOARD
# ---------------------------

fig, axes = plt.subplots(2,2, figsize=(12,10))

sns.barplot(x='Region', y='Total_Sales', data=df, ax=axes[0,0])
axes[0,0].set_title("Sales by Region")

sns.boxplot(x='Region', y='Total_Sales', data=df, ax=axes[0,1])
axes[0,1].set_title("Boxplot")

sns.histplot(df['Total_Sales'], ax=axes[1,0])
axes[1,0].set_title("Sales Distribution")

monthly = df.groupby('Month')['Total_Sales'].sum().reset_index()
sns.lineplot(x='Month', y='Total_Sales', data=monthly, ax=axes[1,1])
axes[1,1].set_title("Monthly Trend")

plt.tight_layout()
plt.savefig("visualizations/subplot_dashboard.png")
plt.show()

# ---------------------------
# 5. INTERACTIVE PLOTLY DASHBOARD
# ---------------------------

fig = px.line(
    df,
    x='Date',
    y='Total_Sales',
    color='Region',
    title="Interactive Sales Trend"
)

fig.write_html("visualizations/interactive_dashboard.html")

fig.show()

print("Dashboard created successfully")
