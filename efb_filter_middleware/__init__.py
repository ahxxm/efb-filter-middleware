# coding=utf-8

import os
import logging
from typing import Optional, Dict, Tuple

from ehforwarderbot import Middleware, Message, utils, Chat
from ehforwarderbot.exceptions import EFBException
from ehforwarderbot.chat import GroupChat, SelfChatMember
import yaml

from enum import Enum

class WorkMode(Enum):
    black_person = "black_persons"
    white_person = "white_persons"
    black_public = "black_publics"
    white_public = "white_publics"
    black_group = "black_groups"
    white_group = "white_groups"


class FilterMiddleware(Middleware):
    middleware_id: str = "ahxxm.filter"
    middleware_name: str = "Filter Middleware"

    mappings: Dict[Tuple[str, str], str] = {}
    chat: Chat = None
    config: Dict = None

    def _reload_config(self):
        config_path = utils.get_config_path(self.middleware_id)
        with open(config_path, encoding="UTF-8") as f:
            self.config = yaml.full_load(f)

    def __init__(self, instance_id: str = None):
        super().__init__(instance_id)

        config_path = utils.get_config_path(self.middleware_id)
        if not os.path.exists(config_path):
            raise EFBException("Filter middleware is not configured.")
        self._reload_config()

        # TODO: only used by super?
        storage_path = utils.get_data_path(self.middleware_id)
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        self.logger = logging.getLogger(self.middleware_id)
        hdlr = logging.FileHandler('./zhangzhishan.filter.log', encoding="UTF-8")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.ERROR)

    def process_message(self, message: Message) -> Optional[Message]:
        # ignore message sent from self
        if isinstance(message.author, SelfChatMember):
            return message

        if self.should_block_message(message):
            return None
        return message

    def should_block_message(self, message: Message) -> bool:
        from_ = message.author.name
        from_alias = message.author.alias
        if from_alias is None:
            from_alias = from_
        if isinstance(message.chat, GroupChat):
            from_ = message.chat.name
            from_alias = message.chat.alias
            if from_alias is None:
                from_alias = from_

        self._reload_config()
        block_names = self.config.get("block_names")
        return from_ in block_names or from_alias in block_names
