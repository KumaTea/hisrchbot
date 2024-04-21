import os
import pickle
from typing import Optional
from datetime import datetime
from bot.session import logging
from dataclasses import dataclass
from pyrogram.types import Message
from share.local import trusted_group
from common.data import msg_data_dir, GROUP_MSG_LIMIT, TRUSTED_GROUP_MSG_LIMIT


@dataclass
class TextMessage:
    id: int
    text: str


@dataclass
class ChatTimeInfo:
    chat_id: int
    last_msg_time: datetime = None
    last_index_time: datetime = None
    last_trigger_time: datetime = None
    trigger_informed: bool = False


def get_text_message(msg: Message) -> Optional[TextMessage]:
    text = msg.text or msg.caption
    if text:
        return TextMessage(msg.id, text)
    return None


class MsgTextStore:
    def __init__(self):
        self.msgs: dict[
            int,  # chat_id
            dict[
                int,  # msg_id
                TextMessage
            ]
        ] = {}
        self.load()

    def raw_add_msg(self, chat_id: int, msg_id: int, text: str) -> None:
        # assert chat_id and msg_id and text
        if chat_id not in self.msgs:
            self.msgs[chat_id] = {}
        self.msgs[chat_id][msg_id] = TextMessage(msg_id, text)

    def add_msg(self, msg: Message) -> None:
        try:
            chat_id = msg.chat.id
            msg_id = msg.id
        except AttributeError:
            return None
        if chat_id not in self.msgs:
            self.msgs[chat_id] = {}
        text_msg = get_text_message(msg)
        if text_msg:
            self.msgs[chat_id][msg_id] = text_msg
    
    def delete_msg(self, msg: Message) -> Optional[bool]:
        try:
            chat_id = msg.chat.id
            msg_id = msg.id
        except AttributeError:
            return None
        if chat_id in self.msgs and msg_id in self.msgs[chat_id]:
            del self.msgs[chat_id][msg_id]
            logging.info(f'[bot.store]\tDeleting message {msg_id} from chat {chat_id}')
            return True

    def update_msg(self, msg: Message) -> None:
        text = msg.text or msg.caption
        if text:
            return self.add_msg(msg)
        else:
            return self.delete_msg(msg)

    def get_msg(self, chat_id: int, msg_id: int) -> Optional[TextMessage]:
        # if chat_id in self.msgs:
        #     if msg_id in self.msgs[chat_id]:
        #         return self.msgs[chat_id][msg_id]
        # return None
        return self.msgs.get(chat_id, {}).get(msg_id, None)

    def clean_all(self) -> None:
        cleaned = 0
        # if len(self.msgs) > 100:
        #     # find last 100 active chats
        #     active_chats = sorted(
        #         self.msgs.keys(),
        #         key=lambda x: max([msg.date for msg in self.msgs[x].values()]),
        #         reverse=True
        #     )[:100]
        #     # clear all other chats
        #     for chat_id in self.msgs:
        #         if chat_id not in active_chats:
        #             del self.msgs[chat_id]
        #             logging.warning(f'[bot.store]\tClearing inactive chat {chat_id}')
        #             cleared += 1

        # for chat_id in self.msgs:
        # https://stackoverflow.com/questions/11941817
        for chat_id in list(self.msgs):
            if not self.msgs[chat_id]:
                del self.msgs[chat_id]
                logging.warning(f'[bot.store]\tClearing empty chat {chat_id}')
                cleaned += 1
                continue

            limit = GROUP_MSG_LIMIT if chat_id not in trusted_group else TRUSTED_GROUP_MSG_LIMIT
            if len(self.msgs[chat_id]) > limit:
                # msg_ids = self.msgs[chat_id].keys()
                msg_ids = list(self.msgs[chat_id])
                msg_ids = sorted(msg_ids)  # int
                trimmed_msg_ids = msg_ids[len(msg_ids) - limit:]

                # self.msgs[chat_id] = {k: v for k, v in self.msgs[chat_id].items() if k in msg_ids}
                for msg_id in list(self.msgs[chat_id]):
                    if msg_id not in trimmed_msg_ids:
                        del self.msgs[chat_id][msg_id]

                logging.warning(f'[bot.store]\tCleaned {len(msg_ids) - limit} messages for chat {chat_id}')
                cleaned += 1
        if cleaned:
            self.save()

    def clear_chat(self, chat_id: int) -> None:
        if chat_id in self.msgs and self.msgs[chat_id]:
            del self.msgs[chat_id]
            # self.msgs[chat_id] = {}
            logging.warning(f'[bot.store]\tDeleting messages for chat {chat_id}')
            self.save()

    def chat_to_json(self, chat_id: int) -> list:
        # return [msg.id for msg in self.msgs.get(chat_id, {}).values()]
        msg_list = [
            {
                'id': msg.id,
                'text': msg.text
            }
            for msg in self.msgs.get(chat_id, {}).values()
        ]
        return msg_list

    def chat_from_json(self, chat_id: int, msg_list: list) -> None:
        self.msgs[chat_id] = {
            msg['id']: TextMessage(msg['id'], msg['text'])
            for msg in msg_list
        }

    def save(self) -> None:
        with open(f'{msg_data_dir}/msg.p', 'wb') as f:
            pickle.dump(self.msgs, f)

    def load(self) -> None:
        if os.path.isfile(f'{msg_data_dir}/msg.p'):
            with open(f'{msg_data_dir}/msg.p', 'rb') as f:
                self.msgs = pickle.load(f)
            logging.info(f'[bot.store]\tLoaded {len(self.msgs)} messages from file')


class MsgTimeStore:
    def __init__(self):
        self.data: dict[
            int,  # chat_id
            ChatTimeInfo
        ] = {}
        self.load()

    def init_chat(self, chat_id: int) -> None:
        if chat_id not in self.data:
            self.data[chat_id] = ChatTimeInfo(chat_id)

    def update_msg_time(self, chat_id: int, msg_time: datetime) -> None:
        self.init_chat(chat_id)
        self.data[chat_id].last_msg_time = msg_time

    def update_index_time(self, chat_id: int, index_time: datetime) -> None:
        self.init_chat(chat_id)
        self.data[chat_id].last_index_time = index_time

    def trigger(self, chat_id: int) -> None:
        self.init_chat(chat_id)
        self.data[chat_id].last_trigger_time = datetime.now()
        self.data[chat_id].trigger_informed = False

    def query(self, chat_id: int) -> ChatTimeInfo:
        if chat_id in self.data:
            return self.data[chat_id]
        return ChatTimeInfo(chat_id)

    def delete(self, chat_id: int) -> None:
        if chat_id in self.data:
            del self.data[chat_id]
            logging.warning(f'[bot.store]\tDeleting time data for chat {chat_id}')
            self.save()

    def save(self) -> None:
        with open(f'{msg_data_dir}/time.p', 'wb') as f:
            pickle.dump(self.data, f)

    # def patch(self) -> None:
    #     if not self.data:
    #         return None
    #     first_chat = list(self.data.keys())[0]
    #     first_info = self.data[first_chat]
    #     if set(first_info.__annotations__) != set(ChatTimeInfo.__annotations__):
    #         logging.warning(f'[bot.store]\tPatching time data')
    #         chat_ids = list(self.data.keys())
    #         for chat_id in chat_ids:
    #             self.data[chat_id] = ChatTimeInfo(
    #                 chat_id=chat_id,
    #                 last_msg_time=getattr(self.data[chat_id], 'last_msg_time', None),
    #                 last_index_time=getattr(self.data[chat_id], 'last_index_time', None),
    #                 last_trigger_time=getattr(self.data[chat_id], 'last_trigger_time', datetime.now())
    #             )
    #         self.save()

    def patch_last_trigger_time(self) -> None:
        if not self.data:
            return None
        patched = 0
        chat_ids = list(self.data.keys())
        for chat_id in chat_ids:
            if not self.data[chat_id].last_trigger_time:
                self.data[chat_id].last_trigger_time = datetime.now()
                logging.warning(f'[bot.store]\tPatching last_trigger_time for chat {chat_id}')
                patched += 1
        if patched:
            self.save()

    def load(self) -> None:
        if os.path.isfile(f'{msg_data_dir}/time.p'):
            with open(f'{msg_data_dir}/time.p', 'rb') as f:
                self.data = pickle.load(f)
            logging.info(f'[bot.store]\tLoaded {len(self.data)} time data from file')
            # self.patch()
            self.patch_last_trigger_time()


text_store = MsgTextStore()
time_store = MsgTimeStore()
