#! /usr/bin/env python3

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

import rethinkdb as r


def save_sync_time(last_sync_time, sync_source, sync_type):
    """Saves sync time for the current data type into the RethinkDB table 'sync_tracker'."""
    sync_entry = {"timestamp": last_sync_time, "source": sync_source, "sync_type": sync_type}
    r.table("sync_tracker").insert(sync_entry).run()
