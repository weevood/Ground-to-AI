#!/usr/bin/env python3
# coding=utf-8

import mysql.connector
from utils.constants import *
from utils.send import send


def open():
    connection = None
    try:
        connection = mysql.connector.connect(user=RDB_USER, password=RDB_PWD, host=RDB_HOST, port=RDB_PORT,database=RDB_NAME)
    except mysql.connector.Error as e:
        send(f"🐞 ERROR: '{e}'")
    return connection


def close(connection):
    try:
        connection.close()
    except mysql.connector.Error as e:
        send(f"🐞 ERROR: '{e}'")


def execute(query, param):
    connection = open()
    cursor = connection.cursor()
    success = False
    try:
        cursor.execute(query, param)
        connection.commit()
        success = True
    except mysql.connector.Error as e:
        send(f"🐞 ERROR: '{e}'")
    finally:
        cursor.close()
        close(connection)
        return success


def select(query):
    connection = open()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        send(f"🐞 ERROR: '{e}'")
    finally:
        cursor.close()
        close(connection)
        return result
