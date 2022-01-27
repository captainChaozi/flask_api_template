FROM chaozi/redoc:v1

WORKDIR /data

COPY . /data

EXPOSE 8080

ENTRYPOINT ["redoc-cli"]

CMD [ "serve", "/data/api.yaml","--host", "0.0.0.0"]