LOAD DATA
INFILE 'C:\Users\pc\Desktop\olist_data\olist_order_reviews_dataset.csv'
INTO TABLE olist_order_reviews
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
 review_id,
 order_id,
 review_score,
 review_comment_title,
 review_comment_message,
 review_creation_date TIMESTAMP "YYYY-MM-DD HH24:MI:SS",
 review_answer_timestamp TIMESTAMP "YYYY-MM-DD HH24:MI:SS"
)
