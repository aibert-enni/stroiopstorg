from rest_framework.pagination import PageNumberPagination


class ProductListPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'paginate_by'
    max_page_size = 24