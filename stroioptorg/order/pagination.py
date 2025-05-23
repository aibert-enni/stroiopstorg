from rest_framework.pagination import PageNumberPagination


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'paginate_by'
    max_page_size = 5