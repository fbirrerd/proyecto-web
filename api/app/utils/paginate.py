# ---------- Helpers ----------
from typing import List, Tuple


def _paginate_list(items_query, page: int = 1, per_page: int = 10) -> Tuple[List, int]:
    total = items_query.count()
    items = items_query.offset((page - 1) * per_page).limit(per_page).all()
    return items, total
