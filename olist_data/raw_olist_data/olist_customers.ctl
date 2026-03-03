LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_customers_dataset.csv'
INTO TABLE olist_customers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 customer_id,
 customer_unique_id,
 customer_zip_code_prefix,
 customer_city,
 customer_state
)
