def test_alembic_migration_file_exists():
    import os
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'alembic', 'versions', '20251219_add_forecasting_tables.py')
    assert os.path.exists(path), "Forecasting migration file should exist"