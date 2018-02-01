CREATE TEMPORARY VIEW SimilarityMatrix AS SELECT f.docid as docid_x, f_T.docid as docid_y, SUM(f.count*f_T.count) as value FROM Frequency f, Frequency f_T WHERE f.term = f_T.term GROUP BY f.docid, f_T.docid;
-- SELECT * FROM SimilarityMatrix WHERE docid_x >= docid_y;
SELECT value FROM SimilarityMatrix WHERE docid_x = '10080_txt_crude' AND docid_y = '17035_txt_earn';
