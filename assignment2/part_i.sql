CREATE TEMPORARY VIEW Query AS
	SELECT 'query' as docid, 'washington' as term, 1 as count UNION
	SELECT 'query' as docid, 'taxes' as term, 1 as count UNION
	SELECT 'query' as docid, 'treasury' as term, 1 as count
;

CREATE TEMPORARY VIEW FrequencyWithQuery AS
	SELECT docid, term, count FROM Frequency UNION
	SELECT docid, term, count FROM Query
;

CREATE TEMPORARY VIEW SimilarityMatrix AS SELECT f.docid as docid_x, f_T.docid as docid_y, SUM(f.count*f_T.count) as value FROM FrequencyWithQuery f, FrequencyWithQuery f_T WHERE f.term = f_T.term GROUP BY f.docid, f_T.docid;
SELECT docid_y, value FROM SimilarityMatrix WHERE docid_x = 'query' ORDER BY value DESC;
