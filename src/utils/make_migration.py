import os
import time
import json
import subprocess

from sqlalchemy import create_engine

from core import config


logger = config.logging.getLogger(__name__)


def save_statement(statement: bool) -> None:
    with open('statement.json', 'w') as file:
        json.dump({'is_done': statement}, file)


def migrate() -> bool:
    if os.path.exists('statement.json'):
        with open('statement.json', 'r') as file:
            statement = json.load(file)
        if statement.get('is_done'):
            return True

    try:
        answer = subprocess.run(["alembic", "revision", "--autogenerate", "-m" "01_initial-db"])
        logger.info("The exit code was: %d" % answer.returncode)
    except Exception as ex:
        logger.error(ex)
    try:
        answer = subprocess.run(["alembic", "upgrade", "head"])
        logger.info("The exit code was: %d" % answer.returncode)
    except Exception as ex:
        logger.error(ex)
        return False
    return True


def wait_db() -> None:
    while True:
        try:
            engine = create_engine('postgresql://app:app@db:5432/urls', pool_pre_ping=True)
            conn = engine.connect()
        except Exception as ex:
            logger.error(ex)
            time.sleep(1)
            continue
        conn.close()
        break


def main():
    wait_db()
    statement = migrate()
    save_statement(statement)


if __name__ == '__main__':
    main()
