#!/usr/bin/bash

docker run --network=host -e SPEC_URL=http://127.0.0.1:5000/apidocs.json redocly/redoc