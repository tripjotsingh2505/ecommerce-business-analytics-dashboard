LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_orders_dataset.csv'
INTO TABLE olist_orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 order_id,
 customer_id,
 order_status,
 order_purchase_timestamp TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 order_approved_at TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 order_delivered_carrier_date TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 order_delivered_customer_date TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 order_estimated_delivery_date TIMESTAMP "YYYY-MM-DD HH24:MI:SS"
)
