import pandas as pd
df = pd.read_csv("C:/Users/Al Kareem Traders/OneDrive/Desktop/Data Science/Final Projects/sales project 2/Data/Late_deliveries.csv")
# print(df)
#                   info about data
# print(df.info())
# print(df.isnull().sum())

#                  sales perfomance analysis
total_price = df["TotalPrice"].sum()
total_quantity_sold = df["Quantity"].sum()
total_orders = df["OrderID"].count()
avg_discount = df["Discount"].mean().round(2)
sales_summary = df.groupby("Product").agg({
    "Quantity": "sum",
    "TotalPrice": "sum",
    "Discount": "mean",
}).reset_index().round(2)

# sales_summary.to_csv("sales_summary.csv", index=False)
# print(sales_summary)
# print(avg_discount)



#                   product analysis
top_selling_product = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(10)
# print(top_selling_product)
product_summary = df.groupby("Product").aggregate({
    "Quantity":"sum",
    "Discount":"sum",
    "TotalPrice":"sum"
}).reset_index()
# product_summary.to_csv("product_summary.csv",index=False)
# print(product_summary)
qty_avg = product_summary["Quantity"].quantile(0.70)
rev_avg = product_summary["TotalPrice"].quantile(0.30)
# print(qty_avg,rev_avg)
high_qty_low_rev = product_summary[(product_summary["Quantity"]>=qty_avg)&(product_summary["TotalPrice"]<=rev_avg)]
# print(high_qty_low_rev) 
product_discount = df.groupby(["Product","Discount"]).aggregate({
    "Quantity":"sum",
    "TotalPrice":"sum"
}).reset_index()
# print(product_discount)
# product_discount.to_csv("product_discount.csv",index=False)




#                   region wise analysis
region_detail = df.groupby("Region")[["RegionManager","StoreLocation","CustomerType","Salesperson"]].first()
# print(region_detail)
best_perfomance_region = df.groupby("Region").aggregate({
    "Quantity":"sum",
    "TotalPrice":"sum",
    "RegionManager":"unique",
    "StoreLocation":"unique",
}).reset_index().sort_values(by="TotalPrice",ascending=False)
# print(best_perfomance_region)
# best_perfomance_region.to_csv("region_performance.csv",index=False)
# region manager perfomance
region_manager_perfomance = df.groupby("RegionManager").aggregate({
    "Region":"unique",
    "Quantity":"sum",
    "Discount":"sum",
    "TotalPrice":"sum",
}).reset_index().sort_values(by="TotalPrice",ascending=False)
# print(region_manager_perfomance)
# region_manager_perfomance.to_csv("region_manger_performance.csv",index=False)
store_loc_wise_sales = df.groupby("StoreLocation").aggregate({
    "Region":"unique",
    "Salesperson":"unique",
    "Quantity":"sum",
    "Discount":"sum",
    "TotalPrice":"sum",
}).reset_index().sort_values(by="TotalPrice",ascending=False).round(2)
# print(store_loc_wise_sales)
# store_loc_wise_sales.to_csv("store_performance.csv",index=False)



#                               customer analysis
customer_type_wise = df.groupby("CustomerType").aggregate({
    "Quantity":"sum",
    "TotalPrice":"sum",
}).reset_index().sort_values(by="TotalPrice",ascending=False).round(3)
# print(customer_type_wise)
# customer_type_wise.to_csv("customer_type_wise.csv",index=False)
high_value_customer = df.groupby("CustomerName").aggregate({
    "Region":"unique",
    "Quantity":"sum",
    "TotalPrice":"sum",
}).reset_index().sort_values(by="TotalPrice",ascending=False).head(20)
# print(high_value_customer)
# high_value_customer.to_csv("high_value_customer.csv",index=False)
ordered_customer = df.groupby("CustomerName").size().reset_index(name="OrderCount")
# print(ordered_customer)
repeated_customer = ordered_customer[ordered_customer["OrderCount"]>1]
# print(repeated_customer.shape[0]) # 124 customer repeated
# repeated_customer.to_csv("repeated_customer.csv",index=False)


#                               Salesperson Performance
high_sales_by_salesperson = df.groupby("Salesperson")["TotalPrice"].sum().reset_index().sort_values(by="TotalPrice",ascending=False)
# high_sales_by_salesperson.to_csv("salesperson_performance.csv",index=False)
# print(high_sales_by_salesperson)
discount_usage_by_salesperson = df.groupby("Salesperson")["Discount"].sum().reset_index().sort_values(by="Discount",ascending=True)
# print(discount_usage_by_salesperson)
total_orders = df.groupby("Salesperson").size()
# print(items_returned)
order_returned = df.groupby("Salesperson")["Returned"].sum()
# print(order_returned)
return_rate_per_person = (order_returned / total_orders)*100
# print(return_rate_per_person)
# return_rate_per_person.to_csv("return_rate_by_salesperson.csv",index=False)



#                               Promotion & Discount Impact
promotion_get_more_sales = df.groupby("Promotion")["TotalPrice"].sum().reset_index().sort_values(by="TotalPrice",ascending=False).round(3)
# print(promotion_get_more_sales)
# promotion_get_more_sales.to_csv("promotion_get_more_sales.csv",index=False)
high_discount_high_sales = df.groupby(["Discount","Product"])["Quantity"].sum().reset_index()
# print(high_discount_high_sales)
# high_discount_high_sales.to_csv("high_discount_high_sales.csv",index=False)
promotion_get_item_return = df.groupby("Promotion")["Returned"].sum().reset_index().sort_values(by="Returned",ascending=False)
# print(promotion_get_item_return)



#                                   Returns & Delivery Analysis
total_products = df.groupby("Product").size()
return_product = df.groupby("Product")["Returned"].sum()
# print(return_product)
return_rate_by_product = (return_product / total_products)*100
# print(return_rate_by_product)
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["DeliveryDate"] = pd.to_datetime(df["DeliveryDate"])

df["DeliveryDays"] = (df["DeliveryDate"]-df["OrderDate"]).dt.days
# print(df[["OrderDate", "DeliveryDate", "DeliveryDays"]].head())
avg_delivery_time = df["DeliveryDays"].mean().round(0)
# print(avg_delivery_time)
late_deliveries = df[df["DeliveryDays"]>6]
total_late_deliveries = late_deliveries.shape[0]
# print(total_late_deliveries)
# total_late_deliveries.to_csv("total_late_deliveries.csv",index=False)
df["On_time_delivery"] = df["DeliveryDays"]<=6
# print(df["On_time_delivery"])
df["LateDelivery"] = df["DeliveryDays"]>6
# print(df["LateDelivery"])
df.to_csv("added_new_column.csv",index=False)



let_deliveries_impact_on_items_return = df.groupby("LateDelivery").aggregate({
    "Returned":"sum"
})
print(let_deliveries_impact_on_items_return)
let_deliveries_impact_on_items_return.to_csv("let_deliveries_impact_on_items_return.csv",index=False)