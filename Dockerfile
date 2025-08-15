FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir bottle

COPY app.py .

EXPOSE 8000

ARG IMAGE_TAG
ENV IMAGE_TAG=${IMAGE_TAG}

CMD ["python", "app.py"]
