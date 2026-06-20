import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
claims = pd.read_csv("claims_data.csv")
food = pd.read_csv("food_listings_data.csv")

# ==========================================
# TIMESTAMP CLEANING
# ==========================================

claims['Timestamp'] = claims['Timestamp'].astype(str)

# dot ko colon me convert karo
claims['Timestamp'] = claims['Timestamp'].str.replace('.', ':', regex=False)

# mixed date formats handle karo
claims['Timestamp'] = pd.to_datetime(
    claims['Timestamp'],
    format='mixed',
    errors='coerce'
)

# standard format
claims['Timestamp'] = claims['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# check invalid dates
print("Invalid Dates:", claims['Timestamp'].isnull().sum())

# cleaned file save
claims.to_csv("claims_data_cleaned.csv", index=False)

print("Timestamp Cleaning Completed")

claims['Date'] = pd.to_datetime(claims['Timestamp']).dt.date
claims['Month'] = pd.to_datetime(claims['Timestamp']).dt.month
claims['Day_Name'] = pd.to_datetime(claims['Timestamp']).dt.day_name()

# ==========================================
# AAGE TUMHARA PURA EDA CODE SAME RAHEGA
# ==========================================

print("Providers shape :", providers.shape)
print("Receivers shape :", receivers.shape)
print("Claims shape :", claims.shape)
print("Food shape :", food.shape)

print(providers.columns)
print(receivers.columns)
print(claims.columns)
print(food.columns)

print(providers.isnull().sum())
print(receivers.isnull().sum())
print(claims.isnull().sum())
print(food.isnull().sum())

print(providers.describe())
print(receivers.describe())
print(claims.describe())
print(food.describe())


# Chart 1: Provider Type Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=providers,
    x='Type'
)

plt.title("Provider Type Distribution")

plt.show()

# Chart 2: Receiver Type Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=receivers,
    x='Type'
)

plt.title("Receiver Type Distribution")
plt.xlabel("Receiver Type")
plt.ylabel("Count")

plt.show()

# Chart 3: Food Type Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=food,
    x='Food_Type'
)

plt.title("Food Type Distribution")
plt.xlabel("Food Type")
plt.ylabel("Count")

plt.show()

# Chart 4: Meal Type Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=food,
    x='Meal_Type'
)

plt.title("Meal Type Distribution")
plt.xlabel("Meal Type")
plt.ylabel("Count")

plt.show()


# Chart 5: City vs Food Listings

plt.figure(figsize=(12, 5))

sns.countplot(
    data=food,
    x='Location'
)

plt.title("City vs Food Listings")
plt.xlabel("City")
plt.ylabel("Food Listings Count")

plt.xticks(rotation=90)

plt.show()

# Chart 6: Top 10 Cities

city_counts = food['Location'].value_counts().head(10)

plt.figure(figsize=(12, 6))

sns.barplot(
    x=city_counts.index,
    y=city_counts.values
)

plt.title("Top 10 Cities by Food Listings")
plt.xlabel("City")
plt.ylabel("Number of Food Listings")

plt.xticks(rotation=45)

plt.show()

# Chart 7: Provider Type vs Quantity

plt.figure(figsize=(8, 5))

sns.barplot(
    data=food,
    x='Provider_Type',
    y='Quantity'
)

plt.title("Provider Type vs Quantity")
plt.xlabel("Provider Type")
plt.ylabel("Quantity")

plt.show()

# Chart 8: Food Type vs Quantity

plt.figure(figsize=(8, 5))

sns.barplot(
    data=food,
    x='Food_Type',
    y='Quantity'
)

plt.title("Food Type vs Quantity")
plt.xlabel("Food Type")
plt.ylabel("Quantity")

plt.show()

# Chart 9: Meal Type vs Quantity

plt.figure(figsize=(8, 5))

sns.barplot(
    data=food,
    x='Meal_Type',
    y='Quantity'
)

plt.title("Meal Type vs Quantity")
plt.xlabel("Meal Type")
plt.ylabel("Quantity")

plt.show()


# Chart 10: Top 10 City vs Provider Type by Quantity


top_cities = food['Location'].value_counts().head(10).index

filtered_food = food[
    food['Location'].isin(top_cities)
]

plt.figure(figsize=(12, 6))

sns.barplot(
    data=filtered_food,
    x='Location',
    y='Quantity',
    hue='Provider_Type'
)

plt.title("Top 10 Cities vs Quantity by Provider Type")

plt.xticks(rotation=45)

plt.show()


# Chart 11: Food Type + Meal Type + Quantity

plt.figure(figsize=(10, 6))

sns.barplot(
    data=food,
    x='Food_Type',
    y='Quantity',
    hue='Meal_Type'
)

plt.title("Food Type vs Quantity by Meal Type")

plt.show()


# Chart 12: Provider + Claims + Quantity

provider_claims = pd.merge(
    food,
    claims,
    on='Food_ID'
)

top_providers = (
    provider_claims
    .groupby('Provider_ID')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=top_providers.index,
    y=top_providers.values
)

plt.title("Top 10 Providers by Quantity Donated")

plt.show()

# Chart 13: Receiver + Claims + Quantity

receiver_claims = pd.merge(
    claims,
    food,
    on='Food_ID'
)

top_receivers = (
    receiver_claims
    .groupby('Receiver_ID')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=top_receivers.index,
    y=top_receivers.values
)

plt.title("Top 10 Receivers by Quantity Claimed")
plt.xlabel("Receiver ID")
plt.ylabel("Total Quantity Claimed")

plt.show()

# Chart 14: Claim Status Distribution

plt.figure(figsize=(8, 5))

sns.countplot(
    data=claims,
    x='Status'
)

plt.title("Claim Status Distribution")

plt.show()

# Chart 15: Top 10 Receivers

top_receivers = claims['Receiver_ID'].value_counts().head(10)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=top_receivers.index,
    y=top_receivers.values
)

plt.title("Top 10 Receivers by Claims")

plt.show()

# Chart 16: Top 10 Food Items Claimed

top_food = claims['Food_ID'].value_counts().head(10)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=top_food.index,
    y=top_food.values
)

plt.title("Top 10 Most Claimed Food Items")

plt.show()
