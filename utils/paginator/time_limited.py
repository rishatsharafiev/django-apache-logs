from django.core.paginator import Paginator
from django.db import connection, transaction, OperationalError
from django.utils.functional import cached_property


class TimeLimitedPaginator(Paginator):
    """
    Paginator that enforced a timeout on the count operation.
    When the timeout is reached a "fake" large value is returned instead,
    Why does this hack exist? On every admin list view, Django issues a
    COUNT on the full queryset. There is no simple workaround. On big tables,
    this COUNT is extremely slow and makes things unbearable. This solution
    is what we came up with.
    """

    @cached_property
    def count(self):
        # We set the timeout in a db transaction to prevent it from
        # affecting other transactions.
        with transaction.atomic():
            try:
                return super().count
            except OperationalError:
                return 9999999999
