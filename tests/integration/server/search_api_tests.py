# Copyright 2018 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
"""Authentication API Endpoint Test"""

import time
import os
import requests

import rethinkdb as r
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

DB_HOST = os.getenv("DB_HOST", "rethink")
DB_PORT = os.getenv("DB_PORT", "28015")
DB_NAME = os.getenv("DB_NAME", "rbac")
DB_CONNECT_TIMEOUT = int(float(os.getenv("DB_CONNECT_TIMEOUT", "1")))

DB_CONNECT_MAX_ATTEMPTS = 5


def connect_to_db():
    """Polls the database until it comes up and opens a connection."""
    connected_to_db = False
    conn = None
    while not connected_to_db:
        try:
            conn = r.connect(host=DB_HOST, port=DB_PORT, db=DB_NAME)
            connected_to_db = True
        except r.ReqlDriverError:
            LOGGER.debug(
                "Could not connect to RethinkDB. Retrying in %s seconds...",
                DB_CONNECT_TIMEOUT,
            )
            time.sleep(DB_CONNECT_TIMEOUT)
    return conn


def create_test_user(session):
    """Create a user and authenticate to use api endpoints during testing."""
    create_user_input = {
        "name": "Susan Susanson",
        "username": "susan20",
        "password": "123456",
        "email": "susan@biz.co",
    }
    session.post("http://rbac-server:8000/api/users", json=create_user_input)


def delete_test_user(username):
    """ Running the new Delete User Query against Rethink DB. """
    conn = connect_to_db()
    (r.table("users").filter({"username": username}).delete().run(conn))
    conn.close()


def test_search_api():
    """Tests the search api endpoint functions and returns a valid payload."""
    with requests.Session() as session:
        create_test_user(session)
        search_query = {
            "query": {
                "search_input": "search input",
                "search_object_types": ["role", "pack", "user"],
                "page_size": "20",
                "page": "2",
            }
        }
        response = session.post("http://rbac-server:8000/api/search", json=search_query)
        assert response.json()["data"] == {"roles": [], "packs": [], "users": []}
        delete_test_user("susan20")
