Added SQLModel-based persistence and Alembic scaffold.

Run the app:

```bash
pip install -r requirements.txt
uvicorn src.app:app --reload
```

To generate a migration (requires alembic):

```bash
alembic revision --autogenerate -m "create activity"
alembic upgrade head
```
