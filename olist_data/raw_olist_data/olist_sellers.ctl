LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_sellers_dataset.csv'
INTO TABLE olist_sellers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 seller_id,
 seller_zip_code_prefix,
 seller_city,
 seller_state
)
