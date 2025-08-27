from app.backend_pre_start import init
from app.core.db import engine


def test_init_successful_connection() -> None:
    try:
        init(engine)
        connection_successful = True
    except Exception:
        connection_successful = False

    assert (
        connection_successful
    ), "The database connection should be successful and not raise an exception."
