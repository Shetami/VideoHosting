from rest_framework.pagination import PageNumberPagination


class PaginationSerials(PageNumberPagination):
    page_size = 1
    max_page_size = 1000


