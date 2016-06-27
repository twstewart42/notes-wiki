# Trials and errors with Docker and onsite docker repo

Great blog on building images http://www.projectatomic.io/docs/docker-building-images/

docker pull docker.example.com:5000/centos7


Get https://docker.example.com:5000/v1/_ping: EOF. If this private registry supports only HTTP or HTTPS with an unknown CA certificate, please add `--insecure-registry docker.example.com:5000` to the daemon's arguments. In the case of HTTPS, if you have access to the registry's CA certificate, no need for the flag; simply place the CA certificate at /etc/docker/certs.d/

Vim /usr/lib/systemd/system/docker.service


<pre>
docker run -d -p 5000:5000 --restart=always -v /nfs/docker:/var/lib/registry/ -v /etc/certs/excert:/certs -e  REGISTRY_HTTP_TLS_CERTIFICATE=/certs/example_all.com.crt -e REGISTRY_HTTP_TLS_KEY=/certs/example.com.key registry:2
</pre>
  curl -XGET https://docker.example.com:5000/v2/_catalog

  docker push docker.example.com:5000/c7-mapserver - worked from client.example.com

https://docs.docker.com/registry/spec/api/


docker build --rm -t local:c7-mapserver .
<pre>
docker run -d --link project-postgr:database -p 8082:80 -v /opt/project/trunk/:/var/www --name project-web local/c7-mapserver


docker run --name project-postgres -d local/postgis-project # runs database

docker run -it --link project-postgres:postgres --rm postgres sh -c 'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U project_db_user projectsustainability' #connect to database

docker run --rm -t -i --name client --link r-Defat_project-httpd_1:server centos:latest /bin/bash 
</pre>
link A bash session of CentOS 7 to a running web server
  psql -h 10.42.211.26 -U project_db_user -wpassword  -d projectdb


start from backend forward:  
run database  
  docker run --name project-postgres -d docker.example.com:5000/project-postgres
Run webserver and link it to database
  docker run -d --link project-postgres:database -p 8082:80 -v /opt/vagrant-example/trunk/project-sustainability:/var/www --name project-web docker.example.com:5000/c7-mapserver-project
Run bash client and link to webserver to test connections
  docker run --rm -t -i --name client --link project-web centos:latest /bin/bash 



builds
write this as 'Dockerfile'
<pre>
FROM centos:7
/opt/c7_prdweb_docker.sh;
RUN curl http://bfesysutl003.example.com/kickstart/ks/c7_prdweb_docker.sh > /tmp/curl_c7.sh && /bin/bash /tmp/curl_c7.sh
EXPOSE 80
VOLUME [ "/var/www" ]
</pre>

