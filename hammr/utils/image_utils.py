# Copyright (c) 2007-2019 UShareSoft, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

def get_uid_from_uri(uri, uid_type):
    args = uri.split("/")
    for index, arg in enumerate(args):
        if arg == uid_type and index + 2 <= len(args):
            return args[index + 1]
    return None

def get_message_from_status(op_status):
    if op_status.error:
        return "Error"
    elif op_status.cancelled:
        return "Cancelled"
    elif op_status.complete:
        return "Done"

    return None
