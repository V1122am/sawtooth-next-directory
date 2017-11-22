# Copyright 2017 Intel Corporation
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
# ------------------------------------------------------------------------------

from sanic import Blueprint
from sanic.response import json

from api.errors import ApiBadRequest
from api.auth import authorized
from api import utils

from db import blocks_query


BLOCKS_BP = Blueprint('blocks')


@BLOCKS_BP.get('api/blocks')
@authorized()
async def get_all_blocks(request):
    head_block_num = await utils.get_request_block_num(request)
    block_resources = await blocks_query.fetch_all_blocks(
        request.app.config.DB_CONN, head_block_num
    )
    return await utils.create_response(
        request.app.config.DB_CONN,
        request.url,
        block_resources,
        head_block_num
    )


@BLOCKS_BP.get('api/blocks/latest')
@authorized()
async def get_latest_block(request):
    if '?head=' in request.url:
        raise ApiBadRequest(
            "Bad Request: 'head' parameter should not be specified"
        )
    block_resource = await blocks_query.fetch_latest_block(
        request.app.config.DB_CONN
    )
    url = request.url.replace('latest', block_resource.get('id'))
    return json({
        'data': block_resource,
        'link': url
    })


@BLOCKS_BP.get('api/blocks/<block_id>')
@authorized()
async def get_block(request, block_id):
    if '?head=' in request.url:
        raise ApiBadRequest(
            "Bad Request: 'head' parameter should not be specified"
        )
    block_resource = await blocks_query.fetch_block_by_id(
        request.app.config.DB_CONN, block_id
    )
    return json({
        'data': block_resource,
        'link': request.url
    })
