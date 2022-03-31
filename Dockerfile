FROM chaozi/python-flask:3.8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 8000

CMD ["/bin/bash","docker_entry.sh"]
