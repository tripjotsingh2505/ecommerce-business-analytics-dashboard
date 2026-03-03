LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_order_payments_dataset.csv'
INTO TABLE olist_order_payments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 order_id,
 payment_sequential,
 payment_type,
 payment_installments,
 payment_value
)
