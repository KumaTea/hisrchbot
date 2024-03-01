import time
import asyncio
from bot.session import meili
from meilisearch.task import TaskInfo


async def until_succeeded(task: TaskInfo, delay: int = 1, timeout: int = 10) -> None:
    status = meili.get_task(task.task_uid)
    t0 = time.time()
    while status.status != 'succeeded':
        await asyncio.sleep(delay)
        status = meili.get_task(task.task_uid)
        if time.time() - t0 > timeout:
            raise TimeoutError(f'Task {task.task_uid} timeout')
