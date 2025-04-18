from django.urls import path

from review.views import ReviewCreateAPIView, ReviewUpdateAPIView, ReviewGetAPIView, ReviewListByMeAPIView, \
    ReviewListByUserIdAPIView, ReviewDeleteAPIView

app_name = 'api-review'

urlpatterns = [
    path('review/<int:pk>/', ReviewGetAPIView.as_view(), name='review-get'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review/update/', ReviewUpdateAPIView.as_view(), name='review_update'),
    path('review/delete/<int:pk>/', ReviewDeleteAPIView.as_view(), name='review_delete'),

    # reviews
    path('reviews/me/', ReviewListByMeAPIView.as_view(), name='review-list-me'),
    path('reviews/user/<int:pk>/', ReviewListByUserIdAPIView.as_view(), name='review-list-user'),
]
