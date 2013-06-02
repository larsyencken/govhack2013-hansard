COPY (
  SELECT
    s.nameid as nameid,
    max(st.name) as name,
    max(st.party) as party,
    max(st.electorate) as electorate,
    s.speech as speech,
    s.time as time
  FROM speeches s join
  session_talkers st
   ON st.nameid = s.nameid
  group by s.nameid, s.speech, s.time
)
TO STDOUT
WITH CSV HEADER
