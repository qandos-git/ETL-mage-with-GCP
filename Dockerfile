FROM python:3.11.2-slim

COPY . /app/

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install  -r requirements.txt

EXPOSE 6789

CMD ["mage", "start", "data-pipeline-project"]
