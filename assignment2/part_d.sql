
SELECT COUNT(*) FROM (
	SELECT DISTINCT docid FROM frequency WHERE (term = "law" AND count > 0) OR (term = "legal" AND count > 0)
)

