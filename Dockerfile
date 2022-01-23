FROM chaozi/python-vim:3.10-flask

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

EXPOSE 8000

CMD ["/bin/bash","docker_entry.sh"]
