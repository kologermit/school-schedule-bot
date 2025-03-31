# Модуль скачивания документа

# Встроенные модули
from os import path
from pathlib import Path

# Внешение модули
from aiogram.types import Message
from openpyxl import load_workbook as open_xlsx, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from xlrd import open_workbook as open_xls

# Внутренние модули
from models import Document
from dispatcher import bot_async
from config import TMP_DIR

async def get_document_by_msg(msg: Message) -> Document:
    file_name = msg.document.file_name.strip().upper()
    file_id = msg.document.file_id
    file_path = path.join(TMP_DIR, file_id+Path(file_name).suffix)
    await bot_async.download(file_id, file_path)
    document = await Document.create(
        name=file_name,
        file_id=file_id,
        message_id=msg.message_id,
        user_id=msg.from_user.id,
        path=file_path,
    )
    await Message.filter(id=msg.message_id, user_id=msg.from_user.id).update(document_id=document.id)
    return document

def get_sheet_by_document(document: Document) -> Worksheet:
    return (
        open_xls(document.path).sheet_by_index(0)
        if document.name.endswith('.XLS') else
        open_xlsx(document.path).active
    )