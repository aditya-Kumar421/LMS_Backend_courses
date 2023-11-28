from django.urls import path
from courses.views import (
    CoursesHomeView,
    CourseDetail,
    SectorCourse,
    SearchCourse,
    AddComment,
    CourseStudy,
    ProductAPI,
    # CartAPI,
)  # , GetCartDetail

urlpatterns = [
    path("products/", ProductAPI.as_view(), name="products"),
    # path("cart/", CartAPI.as_view(), name="cart"),
    path("detail/<uuid:course_uuid>/", CourseDetail.as_view()),
    path("search/<str:search_term>/", SearchCourse.as_view()),
    path("study/<uuid:course_uuid>/", CourseStudy.as_view()),
    path("comment/<course_uuid>/", AddComment.as_view()),
    path("", CoursesHomeView.as_view()),
    path("<uuid:sector_uuid>/", SectorCourse.as_view()),
]
