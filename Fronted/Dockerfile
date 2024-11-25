# FROM httpd:2.4
# COPY index.html /usr/local/apache2/htdocs/

FROM httpd:2.4

# Instalar HAProxy
RUN apt-get update && apt-get install -y haproxy

# Copiar archivos de configuración
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY index.html /usr/local/apache2/htdocs/

# Iniciar Apache y HAProxy
CMD haproxy -f /usr/local/etc/haproxy/haproxy.cfg & httpd-foreground