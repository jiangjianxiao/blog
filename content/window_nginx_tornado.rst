windows 下nginx和tornado 配置
------------------------------

:date: 2012-06-7 13:19
:slug: windows-nginx-tornado



在windows下,nginx和tornado 都可以以残废形容.两者均只能使用select,很多功能都在windows下无法正常运行. 但对于并发用户不高的需求而言,还是可以一试的.

结合nginx和tornado 还是有好处的, 主要是减轻tornado的负担,典型的如让nginx处理静态文件,让nginx处理gzip.由于tornado是单线程的,让nginx进行负载平衡也很有必要.

修改 nginx/conf目录下的nginx.conf ,替换为

说明
======================
1. worker_process 配置为1, 是因为windows下只支持一个工作进程
2. worker_connections 1024就行，因为select有限制


.. code-block:: nginx

	#user  nobody;

	worker_processes  1;
	#daemon off;

	#error_log  logs/error.log;
	#error_log  logs/error.log  notice;
	#error_log  logs/error.log  info;

	pid        logs/nginx.pid;

	events {

	    worker_connections  1024;

	    accept_mutex off;

	}


	http {

	    include       mime.types;

	    default_type  application/octet-stream;

	    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '

	    #                  '$status $body_bytes_sent "$http_referer" '

	    #                  '"$http_user_agent" "$http_x_forwarded_for"';



	    #access_log  logs/access.log  main;



	    sendfile        on;

	    #tcp_nopush     on;

	    keepalive_timeout  65;

	    gzip  on;

	    gzip_min_length  1000;

	    gzip_buffers     4 8k;

	    gzip_types text/plain application/json application/x-javascript text/css application/xml text/javascript image/jpeg image/gif image/png;

	    proxy_next_upstream error;



	    upstream tornadoes{

	    	server 127.0.0.1:8000;

	        server 127.0.0.1:8001;

	  

	    }

	    server {

	        listen       80;

	        server_name  localhost;

		    location /static/{

		        root 你的静态文件根目录

		    }

	        location /{

	            proxy_pass_header Server;

	            proxy_set_header Host $http_host;

	            proxy_redirect off;

	            proxy_set_header X-Real-IP $remote_addr;

	            proxy_set_header X-Scheme $scheme;

	            proxy_pass http://tornadoes;



	        }

	    }


	}


延伸: 关于worker_processes/worker_connections
=========================================================

默认为1024

在纯nginx下，web服务器的最大访问客户数 max clients = worker_processes 乘以worker_connections。

nginx作为反向代理的时候 max clients = worker_processes 乘以worker_connections 再除以4。

worker_processes 一般等于CPU的内核数目

配置 worker_processes时一般同时配置event中的 worker_rlimit_nofile, worker_processes 不超过worker_rlimit_nofile


延伸: daemon off;
====================================

如果使用supervisor 管理nginx进程，需要加上, windows下如果使用srvany.exe， 也需要(这个待验证！)
