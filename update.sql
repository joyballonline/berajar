update f_proxy_pool_tab set isactive=0 where isactive in (8,9) and use_count > -1;
