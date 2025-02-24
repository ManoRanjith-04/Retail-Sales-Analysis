import pandas as pd
df=pd.read_csv("C://Users//Mano Ranjith//Downloads//orders.csv")
df
# Checking null values
print(df.isnull().sum())
# Renaming the columns and trimming the Extra spaces
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)
df['ship_mode']= df['ship_mode'].fillna("Not Available")
df
# Calculating Discounts
df['discount_amount'] = (df['list_price'] * df['discount_percent']) / 100
df['sale_price'] = df['list_price'] - df['discount_amount']
df['profit'] = (df['sale_price'] - df['cost_price']) 
df
# Spliting the single dataset into two different dataset
order1 = df[['order_id', 'order_date', 'ship_mode', 'segment', 'country', 'city', 'state', 
             'postal_code', 'region']].drop_duplicates()
order2 = df[['order_id', 'product_id', 'category', 'sub_category', 'cost_price', 
               'list_price', 'quantity', 'discount_percent', 'discount_amount', 
               'sale_price', 'profit']]
order1.set_index("order_id", inplace=True)
order2.set_index("product_id", inplace=True)
order1.to_csv("order1.csv")
order2.to_csv("order2.csv")

**********************************************SQL*****************************************************
create database Retail_order;
use retail_order;
select * from order1;
select * from order2;

#Top-Selling Products
select product_id, category, SUM(sale_price * quantity) as total_revenue
from order2
group by product_id, category
order by total_revenue desc
limit 10;

#Monthly Sales Analysis
select 
    year(order_date) as Year, 
    month(order_date) as Month, 
    sum(sale_price * quantity) as total_sales
from order1 as a
join order2 as b on a.order_id = b.order_id
group by year(order_date), month(order_date)
order by year, month;

#Product Performance
select 
    product_id, 
    category,
    sum(sale_price * quantity) as total_revenue,
    sum(profit) as total_profit,
    (sum(profit) / sum(sale_price * quantity)) * 100 as profit_margin,
    row_number() over (order by SUM(profit) desc) as Top_performance
from order2
group by product_id, category
order by total_profit desc;

#Regional Sales Analysis
select 
    region, 
    sum(sale_price * quantity) as total_revenue, 
    sum(profit) as total_profit
from order1 as a
join order2 as b on a.order_id = b.order_id
group by region
order by total_revenue desc;

#Discount Analysis
select 
    product_id, 
    category, 
    discount_percent, 
    sum(sale_price * quantity) as total_sales,
    sum(profit) as total_profit
from order2
where discount_percent < 10
group by product_id, category, discount_percent
order by discount_percent desc;

#QUERIES
#1. Top 10 Highest Revenue Generating Products
select product_id,category,sum(sale_price*quantity) as Total_revenue
from order2
group by product_id, category
order by Total_revenue desc
limit 10;

#2. Find the top 5 cities with the highest profit margins
select city,
(sum(profit)/sum(sale_price*quantity)) as profit_margins
from order1 as a inner join order2 as b on a.order_id=b.order_id
group by city
order by profit_margins desc
limit 5;

#3. Calculate the total discount given for each category
select category, sum(discount_amount) as Total_discount
from order2
group by category
order by Total_discount desc;

#4. Find the average sale price per product category
select category, avg(sale_price) as Average_sales_price
from order2
group by category
order by average_sales_price desc;

#5. Find the region with the highest average sale price
select region,
avg(sale_price) as Avg_sale_price_Region
from order1 as a join order2 as b on a.order_id-b.order_id
group by region
order by  Avg_sale_price_Region desc
limit 1;

#6. Find the total profit per category
select category,
sum(profit) as Total_profit from order2
group by category
order by Total_profit desc;

#7.  Identify the top 3 segments with the highest quantity of orders
select segment,
sum(quantity) as Highest_quantity
from order1 as a join order2 as b on a.order_id=b.order_id
Group by segment
order by Highest_quantity desc;

#8. Determine the average discount percentage given per region
select region, avg(discount_percent) as Avg_Discount_Percentage
from order1 as a join order2 as b on a.order_id=b.order_id
group by region
order by Avg_Discount_Percentage desc;

#9. Find the product category with the highest total profit
select category,sum(profit) as Total_profit
from order2
group by category
order by Total_profit desc;

#10. Calculate the total revenue generated per year
select year(order_date) as Year, sum(sale_price*quantity) as Total_revenue
from order1 as a join order2 as b on a.order_id=b.order_id
group by year(order_date)
order by Year asc;

#11. Find the Month with the Highest Sales Volume
select month(order_date) as Month, count(order_id) as Total_order
from order1
group by month(order_date)
order by Total_order desc
limit 1;

#12. Identify Products with More Than 3% Discount
select product_id, category, discount_percent 
from order2
where discount_percent>3
order by discount_percent desc;

#13. Find the Most Commonly Ordered Product
select product_id, count(order_id) as Frequently_ordered_product
from order2
group by product_id
order by Frequently_ordered_product desc
limit 1;

#14. Find the Region with the Highest Total Orders
select region, count(order_id) as Total_orders
from order1
group by region
order by Total_orders desc
limit 1;

#15. Calculate the Total Discount Given Per Year
select year(order_date) as Year, sum(discount_amount) as Total_discount
from order1 as a inner join order2 as b on a.order_id=b.order_id
group by year(order_date)
order by Year;

#16. Identify the Least Profitable Product
select product_id, sum(profit) as Least_profit
from order2
group by product_id
order by Least_profit asc
limit 1;

#17. Find the Average Order Value (AOV) Per Region
select region, avg(sale_price*quantity) as Avg_order_value
from order1 as a join order2 as b on a.order_id=b.order_id
group by region
order by Avg_order_value desc;

#18. Rank Top 5 Products by Profit Margin
select product_id, category,
(sum(profit)/sum(sale_price))*100 as profit_margin,
row_number() over(order by (sum(profit)/sum(sale_price))desc) as Top_product
from order2
group by product_id,category
order by profit_margin desc
limit 5;

#19 Find the Category with the Most Orders
select category,count(order_id) as most_orders
from order2
group by category
order by most_orders desc
limit 1;

#20 Calculate Total Revenue and Profit Per Customer Segment
select segment, sum(sale_price * quantity) as Total_revenue, sum(profit) as Total_profit
from order1 as a join order2 as b on a.order_id=b.order_id
group by segment
order by Total_revenue desc;

********************************************STREAMLIT UI***********************************************
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Mano1426$',
        database='retail_order'
    )

# Query dictionary with titles
queries = {
    "Top 10 Highest Revenue Products": "select product_id, category, sum(sale_price*quantity) as Total_revenue from order2 group by product_id, category order by Total_revenue desc limit 10;",
    "Top 5 Cities with Highest Profit Margins": "select city, (sum(profit)/sum(sale_price*quantity)) as profit_margins from order1 as a inner join order2 as b on a.order_id=b.order_id group by city order by profit_margins desc limit 5;",
    "Total Discount Given per Category": "select category, sum(discount_amount) as Total_discount from order2 group by category order by Total_discount desc;",
    "Average Sale Price per Category": "select category, avg(sale_price) as Average_sales_price from order2 group by category order by Average_sales_price desc;",
    "Region with Highest Average Sale Price": "select region, avg(sale_price) as Avg_sale_price_Region from order1 as a join order2 as b on a.order_id=b.order_id group by region order by Avg_sale_price_Region desc limit 1;",
    "Total Profit per Category": "select category,sum(profit) as Total_profit from order2 group by category order by Total_profit desc;",
    "Top 3 Segments with the Highest Quantity of Orders": "select segment,sum(quantity) as Highest_quantity from order1 as a join order2 as b on a.order_id=b.order_id Group by segment order by Highest_quantity desc;",
    "Average Discount Percentage given per Region": "select region, avg(discount_percent) as Avg_Discount_Percentage from order1 as a join order2 as b on a.order_id=b.order_id group by region order by Avg_Discount_Percentage desc;",
    "Product Category with the Highest Total Profit": "select category,sum(profit) as Total_profit from order2 group by category order by Total_profit desc;",
    "Total Revenue Generated per Year": "select year(order_date) as Year, sum(sale_price*quantity) as Total_revenue from order1 as a join order2 as b on a.order_id=b.order_id group by year(order_date) order by Year asc;",
    "Month with the Highest Sales Volume": "select month(order_date) as Month, count(order_id) as Total_order from order1 group by month(order_date) order by Total_order desc limit 1;",
    "Products with more than 3% Discount": "select product_id, category, discount_percent  from order2 where discount_percent>3 order by discount_percent desc;",
    "Most Commonly Ordered Product": "select product_id, count(order_id) as Frequently_ordered_product from order2 group by product_id order by Frequently_ordered_product desc limit 1;",
    "Region with the Highest Total Orders": "select region, count(order_id) as Total_orders from order1 group by region order by Total_orders desc limit 1;",
    "Calculate the Total Discount given per Year": "select year(order_date) as Year, sum(discount_amount) as Total_discount from order1 as a inner join order2 as b on a.order_id=b.order_id group by year(order_date) order by Year;",
    "Least Profitable Product": "select product_id, sum(profit) as Least_profit from order2 group by product_id order by Least_profit asc limit 1;",
    "Average Order Value (AOV) Per Region": "select region, avg(sale_price*quantity) as Avg_order_value from order1 as a join order2 as b on a.order_id=b.order_id group by region order by Avg_order_value desc;",
    "Top 5 Products by Profit Margin": "select product_id, category, (sum(profit)/sum(sale_price))*100 as profit_margin, row_number() over(order by (sum(profit)/sum(sale_price))desc) as Top_product from order2 group by product_id,category order by profit_margin desc limit 5;",
    "Category with the Most Orders": "select category,count(order_id) as most_orders from order2 group by category order by most_orders desc limit 1;",
    "Total Revenue and Profit per Customer Segment": "select segment, sum(sale_price * quantity) as Total_revenue, sum(profit) as Total_profit from order1 as a join order2 as b on a.order_id=b.order_id group by segment order by Total_revenue desc;"
}

# Streamlit UI
st.sidebar.title("📊 Sales Analysis Dashboard")
selected_query = st.sidebar.selectbox("🔍Select a Query", list(queries.keys()))

# Run selected query
def run_query(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Display query results
data = run_query(queries[selected_query])
st.write(f"### Results for: {selected_query}")
st.dataframe(data)

# Data Visualization
if selected_query == "Top 10 Highest Revenue Products":
    fig = px.bar(data, x='product_id', y='Total_revenue', color='category', title='Top 10 Revenue Generating Products')
elif selected_query == "Top 5 Cities with Highest Profit Margins":
    fig = px.line(data, x='city', y='profit_margins', title='Top 5 Cities with Highest Profit Margins')
elif selected_query == "Total Discount Given per Category":
    fig = px.pie(data, names='category', values='Total_discount', title='Total Discount Given per Category')
elif selected_query == "Average Sale Price per Category":
    fig = px.bar(data, x='category', y='Average_sales_price', title='Average Sale Price per Category')
elif selected_query == "Region with Highest Average Sale Price":
    fig = px.scatter(data, x='region', y='Avg_sale_price_Region', size='Avg_sale_price_Region', title='Region with Highest Avg Sale Price')
elif selected_query == "Total Profit per Category":
    fig = px.bar(data, x='category', y='Total_profit', title='Total Profit Per Category')
elif selected_query == "Segments with the Highest Quantity of Orders":
    fig = px.line(data, x='segment', y='quantity', title='Segments with Highest Quantity of Orders')
elif selected_query == "Average Discount Percentage given per Region":
    fig = px.line(data, x='region', y='Avg_Discount_Percentage', title='Average Discount Per Region')
elif selected_query == "Category with the Highest Total Profit":
    fig = px.line(data, x='category', y='Total_profit', title='Category with the Highest Total Profit')
elif selected_query == "Total Revenue Generated per Year":
    fig = px.line(data, x='Year', y='Total_revenue', title='Total Revenue Generated per Year')
elif selected_query == "Month with the Highest Sales Volume":
    fig = px.scatter(data, x='Month', y='Total_order', title='Month with the Highest Sales Volume')
elif selected_query == "Products with more than 3% Discount":
    fig = px.bar(data, x='product_id', y='discount_percent', color='category', title='Products with more than 3% Discount')
elif selected_query == "Most Commonly Ordered Product":
    fig = px.scatter(data, x='product_id', y='Frequently_ordered_product', title='Most Commonly Ordered Product')
elif selected_query == "Region with the Highest Total Orders":
    fig = px.scatter(data, x='region', y='Total_orders', title='Region with the Highest Total Orders')
elif selected_query == "Total Discount given per Year":
    fig = px.bar(data, x='Year', y='Total_discount', title='Total Discount Given per Year')
elif selected_query == "Least Profitable Product":
    fig = px.line(data, x='product_id', y='Least_profit', title='Least Profitable Product')
elif selected_query == "Average Order Value (AOV) Per Region":
    fig = px.scatter(data, x='region', y='Avg_order_value', title='Average Order Value (AOV)')
elif selected_query == "Top 5 Products by Profit Margin":
    fig = px.pie(data, names='product_id', values='profit_margin', color='category', title='Top 5 Products by Profit Margin')
elif selected_query == "Category with the Most Orders":
    fig = px.scatter(data, x='category', y='most_orders', title='Category with the Most Orders')
elif selected_query == "Total Revenue and Profit per Customer Segment":
    fig = px.bar(data, x='Total_revenue', y='Total_profit', color='segment', title='Total Revenue and Profit per Customer Segment')

else:
    fig = px.line(data, x=data.columns[0], y=data.columns[1], title=selected_query)

st.plotly_chart(fig)












