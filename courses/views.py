from .serializers import CourseDisplaySerializer, CourseUnpaidSerializer, CourseListSerailizer, CommentSerializer,CoursePaidSerializer, ProductSerializer

from courses.models import Sector, Course,Cart
from users.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.db.models import Q

class CoursesHomeView(APIView):
    def get(self, request, *args, **kwargs):
        sectors=Sector.objects.order_by("?")[:6]

        sector_response=[]

        for sector in sectors:
            sector_courses=sector.related_course.order_by("?")[:4]
            courses_serializer=CourseDisplaySerializer(sector_courses, many=True)

            sector_obj={
                'sector_name':sector.name,
                'sector_uuid':sector.sector_uuid,
                'featured_course':courses_serializer.data,
                'sector_image':sector.get_image_absolute_url()
            }

            sector_response.append(sector_obj)
        
        return Response(data=sector_response, status=status.HTTP_200_OK)

class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course =Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest('course does not exist')

        serializer=CourseUnpaidSerializer(course[0])

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector=Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest('Sector does not exist')
        
        sector_courses=sector[0].related_course.all()
        serializer=CourseListSerailizer(sector_courses, many=True)

        total_students=0
        for course in sector_courses:
            total_students+=course.get_enrolled_student()

        return Response({
            'data':serializer.data,
            'sector_name': sector[0].name,
            'total_students':total_students,
            },status=status.HTTP_200_OK )
    
class SearchCourse(APIView):

    def get(self, request, search_term):
        matches=Course.objects.filter(Q(title__icontains=search_term))     
        serializer=CourseListSerailizer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class AddComment(APIView):
    def post(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course does not exist')

        content = request.data  

        if not content.get('message'):
            return Response("Message field is required", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=content)

        if serializer.is_valid():
            author = User.objects.get(id=1)  
            comment = serializer.save(user=author)
            course.comments.add(comment)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseStudy(APIView):
    def get(self,request, course_uuid ):
        try:
            course=Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('course Does not exist')

        request.user = User.objects.get(id=1)
        user_course = request.user.paid_courses.filter(course_uuid=course_uuid)
        if not user_course:
            return HttpResponseNotAllowed('User does not own this course')

        serializer= CoursePaidSerializer(course)

        return Response(serializer.data, status = status.HTTP_200_OK)

class CartAPI(APIView):
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        qs = Cart.objects.all()
        return Response(
            {"data": self.serializer_class(qs, many=True).data}, 
            status=status.HTTP_200_OK
            )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Added into cart successfully"}, 
            status=status.HTTP_201_CREATED
            )
    