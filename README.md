```bash
docker run --name canchita-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=canchita_sas_db -p 5432:5432 -d postgres:15-alpine
python -m pip install -r requirements.txt
```