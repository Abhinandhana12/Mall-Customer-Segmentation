# ==========================================================
# Mall Customer Segmentation using K-Means Clustering
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import os

# ==========================================================
# STEP 1 : Load Dataset
# ==========================================================

filename = "Mall_Customers.csv"

if not os.path.exists(filename):
    print(f"Error: {filename} not found!")
    exit()

df = pd.read_csv(filename)

print("\n========== DATASET LOADED ==========")
print(df.head())

# ==========================================================
# STEP 2 : Dataset Information
# ==========================================================

print("\n========== DATA INFO ==========")
print(df.info())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# ==========================================================
# STEP 3 : Handle Missing Values
# ==========================================================

# Fill missing Gender
if "Gender" in df.columns:
    df["Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])

# Fill missing Age
if "Age" in df.columns:
    df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill missing Annual Income
df["Annual Income (k$)"] = df["Annual Income (k$)"].fillna(
    df["Annual Income (k$)"].median()
)

# Fill missing Spending Score
df["Spending Score (1-100)"] = df["Spending Score (1-100)"].fillna(
    df["Spending Score (1-100)"].median()
)

print("\nMissing Values After Cleaning")
print(df.isnull().sum())

# ==========================================================
# STEP 4 : Exploratory Data Analysis
# ==========================================================

plt.figure(figsize=(6,4))
sns.histplot(df["Age"], bins=20, kde=True)
plt.title("Age Distribution")
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df["Annual Income (k$)"], bins=20, kde=True)
plt.title("Annual Income Distribution")
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df["Spending Score (1-100)"], bins=20, kde=True)
plt.title("Spending Score Distribution")
plt.show()

# ==========================================================
# STEP 5 : Correlation Heatmap
# ==========================================================

numeric_df = df.select_dtypes(include="number")

plt.figure(figsize=(7,5))
sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.show()

# ==========================================================
# STEP 6 : Feature Selection
# ==========================================================

X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

# ==========================================================
# STEP 7 : Elbow Method
# ==========================================================

wcss = []

for i in range(1,11):

    model = KMeans(
        n_clusters=i,
        init="k-means++",
        random_state=42,
        n_init=10
    )

    model.fit(X)

    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1,11), wcss, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# ==========================================================
# STEP 8 : Apply K-Means
# ==========================================================

kmeans = KMeans(
    n_clusters=5,
    init="k-means++",
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X)

# ==========================================================
# STEP 9 : Cluster Centers
# ==========================================================

print("\n========== CLUSTER CENTERS ==========")
print(kmeans.cluster_centers_)

# ==========================================================
# STEP 10 : Cluster Summary
# ==========================================================

summary = df.groupby("Cluster").mean(numeric_only=True)

print("\n========== CLUSTER SUMMARY ==========")
print(summary)

# ==========================================================
# STEP 11 : Assign Cluster Names
# ==========================================================

cluster_names = {
    0: "Cluster 0",
    1: "Cluster 1",
    2: "Cluster 2",
    3: "Cluster 3",
    4: "Cluster 4"
}

df["Cluster Name"] = df["Cluster"].map(cluster_names)

# ==========================================================
# STEP 12 : Scatter Plot
# ==========================================================

plt.figure(figsize=(9,6))

sns.scatterplot(
    data=df,
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    hue="Cluster",
    palette="Set1",
    s=90
)

plt.scatter(
    kmeans.cluster_centers_[:,0],
    kmeans.cluster_centers_[:,1],
    marker="X",
    s=300,
    color="black",
    label="Centroids"
)

plt.title("Mall Customer Segmentation")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.legend()
plt.grid(True)

plt.show()

# ==========================================================
# STEP 13 : Save Output
# ==========================================================

df.to_csv("clustered_customers.csv", index=False)

print("\n======================================")
print("PROJECT EXECUTED SUCCESSFULLY")
print("======================================")

print("\nOutput File Created:")
print("clustered_customers.csv")

print("\nFirst 10 Records")

print(df.head(10))

