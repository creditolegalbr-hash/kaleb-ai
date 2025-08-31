import os
import sqlite3
import time
from typing import Any, Dict

from .base_adapter import BaseAdapter


class DatabaseAdapter(BaseAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.service_name = "database"
        self.connection = None
        self.db_path = config.get("path", "automation.db")
        self._connect()

    def _connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.logger.info(f"Connected to database: {self.db_path}")
            self._initialize_tables()
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def _initialize_tables(self):
        """Initialize database tables"""
        try:
            cursor = self.connection.cursor()

            # Create tasks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_type TEXT NOT NULL,
                    task_description TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create memories table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    task TEXT NOT NULL,
                    result TEXT NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            self.connection.commit()
            self.logger.info("Database tables initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize tables: {str(e)}")
            raise

    def execute(self, request: dict) -> dict:
        """Execute database request"""
        try:
            self.logger.info(
                f"Executing database request: {request.get('method', 'query')}"
            )

            method = request.get("method", "query")
            if method == "query":
                result = self._execute_query(request)
            elif method == "insert":
                result = self._insert_record(request)
            elif method == "update":
                result = self._update_record(request)
            else:
                raise ValueError(f"Unknown database method: {method}")

            return {"status_code": 200, "data": result}

        except Exception as e:
            self.logger.error(
                f"Error executing database request: {str(e)}", exc_info=True
            )
            return {"status_code": 500, "error": str(e)}

    def _execute_query(self, request: dict) -> dict:
        """Execute database query"""
        query = request.get("query", "")
        params = request.get("params", ())

        self.logger.debug(f"Executing query: {query}")

        cursor = self.connection.cursor()
        cursor.execute(query, params)

        # For SELECT queries, fetch results
        if query.strip().upper().startswith("SELECT"):
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            result = {"columns": columns, "rows": rows}
        else:
            # For INSERT/UPDATE/DELETE, commit and return row count
            self.connection.commit()
            result = {"rowcount": cursor.rowcount}

        return result

    def _insert_record(self, request: dict) -> dict:
        """Insert record into table"""
        table = request.get("table", "")
        data = request.get("data", {})

        if not table or not data:
            raise ValueError("Table name and data are required for insert")

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())

        self.logger.debug(f"Inserting into {table}: {data}")

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

        return {"id": cursor.lastrowid, "rowcount": cursor.rowcount}

    def _update_record(self, request: dict) -> dict:
        """Update record in table"""
        table = request.get("table", "")
        data = request.get("data", {})
        where = request.get("where", {})

        if not table or not data or not where:
            raise ValueError(
                "Table name, data, and where clause are required for update"
            )

        # Build SET clause
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        set_params = list(data.values())

        # Build WHERE clause
        where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
        where_params = list(where.values())

        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = set_params + where_params

        self.logger.debug(f"Updating {table}: {data} where {where}")

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

        return {"rowcount": cursor.rowcount}

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")
