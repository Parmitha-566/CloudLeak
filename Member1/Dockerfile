
FROM python:3.12-slim

WORKDIR /app

COPY sample_billing.csv .
COPY cloud_resource_module.py .

ENTRYPOINT ["python", "cloud_resource_module.py"]