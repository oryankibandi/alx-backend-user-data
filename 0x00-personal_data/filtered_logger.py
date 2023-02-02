#!/usr/bin/env python3
"""Filter Logger"""

import os
import logging
import re
import typing
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: typing.List[str], redaction: str, message: str, separator: str) -> str:
    """filters log messages"""
    secret_words = [item.split('=')[1] for item in message.split(
        separator) if fields.count(item.split('=')[0]) != 0]
    reg_exp = r"\b(" + "|".join(secret_words) + r")\b"
    return re.sub(reg_exp, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format incoming strings"""
        record.msg = filter_datum(
            self._fields, self.REDACTION, record.msg, self.SEPARATOR)
        return self.formatMessage(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logging.basicConfig(level=logging.INFO, format=RedactingFormatter)
    return logging.Logger("user_data", )


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to a MySQL database"""
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME") | "root",
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD") | "",
        host=os.getenv("PERSONAL_DATA_DB_HOST") | "localhost",
        database=os.getenv("PERSONAL_DATA_DB_NAME") | "holberton"
    )
    return connection


def main() -> None:
    """queries a mysql db"""
    connection = get_db()
    cursor = connection.cursor()
    fields = ['name', 'email', 'phone', 'ssn', 'password']
    query = ("SELECT * FROM users")
    cursor.execute(query)
    for row in cursor:
        print(filter_datum(fields, '***', row, ';'))

    connection.close()
