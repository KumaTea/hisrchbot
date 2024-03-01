import logging
from bot.session import meili
from dataclasses import dataclass
from meilisearch.errors import MeilisearchApiError


@dataclass
class SearchResult:
    success: bool
    results: list[dict] = None
    failed_reason: str = None


def search_core(chat_id: int, query_term: str, exact_search: bool = True, limit: int = 10) -> SearchResult:
    if not query_term:
        return SearchResult(success=False, failed_reason='Empty query term')

    index = meili.index(chat_id)
    try:
        search_params = {'limit': limit}
        if exact_search:
            search_params['matchingStrategy'] = 'all'
        # search_task = index.search(query_term, search_params)
        # This doesn't return TaskInfo
        search_result = index.search(query_term, search_params)
        return SearchResult(success=True, results=search_result['hits'])
    except MeilisearchApiError as e:
        # if e.code == 'index_not_found':
        if 'index_not_found' in str(e):
            return SearchResult(success=False, failed_reason='本群尚未被收录，请正常群聊，等待至少1小时以完成索引。')
        else:
            logging.error(f'Search error: {e}')
            return SearchResult(success=False, failed_reason=str(e))
