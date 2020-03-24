FROM nginx
ADD dist /usr/share/nginx/html/
ADD nginx.conf /etc/nginx
EXPOSE 8091
CMD ["nginx","-g","daemon off;"]
