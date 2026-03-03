LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_order_items_dataset.csv'
INTO TABLE olist_order_items
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 order_id,
 order_item_id,
 product_id,
 seller_id,
 shipping_limit_date TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 price,
 freight_value
)
