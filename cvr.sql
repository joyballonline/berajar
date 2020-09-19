select to_char(x.get_datetime,'yyyymmdd'), x.status_code, count(*) 
from f_get_url_log_tab x where to_char(x.get_datetime,'yyyymmdd') > '20200915'
and status_code in (200,2000) 
group by to_char(x.get_datetime,'yyyymmdd'),x.status_code order by 1,2