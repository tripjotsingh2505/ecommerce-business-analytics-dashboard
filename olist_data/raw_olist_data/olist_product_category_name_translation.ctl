LOAD DATA
INFILE 'product_category_name_translation.csv'
INTO TABLE product_category_name_translation
APPEND
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
  product_category_name,
  product_category_name_english
)
