
SELECT COUNT(*) FROM (
	SELECT docid FROM frequency GROUP BY docid HAVING sum(count) > 300
) x;
