from .serializers import CourseDisplaySerializer, CourseUnpaidSerializer, CourseListSerailizer, CommentSerializer,CoursePaidSerializer, ProductSerializer#, CartItemserializer

from courses.models import Sector, Course,Cart
from users.models import User
# from courses.service import Cart

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.db.models import Q

import json
from decimal import Decimal

#Dashboard for courses
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
                #change
                # 'sector_image':sector.get_image_absolute_url()
            }

            sector_response.append(sector_obj)
        
        return Response(data=sector_response, status=status.HTTP_200_OK)

#Details of courses
class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course =Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest('course does not exist')

        serializer=CourseUnpaidSerializer(course[0])

        return Response(data=serializer.data, status=status.HTTP_200_OK)

#categories for courses
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
    
#Search bar for courses:
class SearchCourse(APIView):

    def get(self, request, search_term):
        matches=Course.objects.filter(Q(title__icontains=search_term))      #| Q(description__icontains=search_term)
        serializer=CourseListSerailizer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

#Comment section in detail of course:
class AddComment(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course does not exist')

        try:
            content = json.loads(request.body)   

        except json.decoder.JSONDecodeError:
            return Response("Please a json body", status= status.HTTP_400_BAD_REQUEST)

        if not content.get('message'):
            return Response(status= status.HTTP_400_BAD_REQUEST)
        
        serializer=CommentSerializer(data=content)

        if serializer.is_valid():
            author=User.objects.get(id=1)
            comment = serializer.save(user = author)
            # comment = serializer.save(user = request.user)
            course.comments.add(comment)
            return Response(status=status.HTTP_201_CREATED )
        else:
            return Response(data=serializer.errors,status =status.HTTP_400_BAD_REQUEST)

#adding to cart courses:
#class GetCartDetail(APIView):
    # def get(self, request):
    #     cart_items = Course.objects.filter(user=request.user)
    #     serializer = CartItemserializer(cart_items, many=True)
    #     return Response(serializer.data)
    
    # def post(self,request,*args, **kwargs):

    #     try:
    #         body =  json.loads(request.body)
        
    #     except json.decoder.JSONDecodeError:
    #         return HttpResponseBadRequest()

    #     if type(body.get('cart')) != list:
    #         return HttpResponseBadRequest()

    #     if len(body.get("cart")) ==0:
    #         return Response(data=[])

    #     courses=[]

    #     for uuid in body.get("cart"):
    #         item = Course.objects.filter(course_uuid=uuid)

    #         if not item:
    #             return HttpResponseBadRequest()
            
    #         courses.append(item[0])

    #         # serializer for cart
    #     serializer =CartItemserializer(courses,many=True)

    #     #TODO : After you have added the price field
    #     cart_cost=Decimal(0.00)

    #     for item in serializer.data:
           
    #         cart_cost+=Decimal(item.get("price"))

    #     return Response(data={"cart_detail":serializer.data,"cart_total":str(cart_cost)})

    # def get(self, request):
    #     cart_items = CartItem.objects.filter(user=request.user)
    #     serializer = CartItemserializer(cart_items, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = CartItemserializer(data=request.data)
    #     if serializer.is_valid():
    #         cart_total = Decimal(0.00)
    #         for item in serializer.data:
    #             cart_total+=Decimal(item.get('price'))
    #         serializer.save(user=request.user)
    #         return Response(data={
    #         'cart_detail':serializer.data,
    #         'cart_total':cart_total
    #     }, status = status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#adding with get and post both:
# class CartItemList(APIView):
    
#     def post(self, request, *args, **kwargs):
#         try:
#             body = json.loads(request.body)
#         except json.decoder.JSONDecodeError:
#             return HttpResponseBadRequest()

#         if type(body.get('cart')) != list:
#             return HttpResponseBadRequest()

#         cart_uuids = body.get("cart")
#         if len(cart_uuids) == 0:
#             return Response(data=[])

#         cart_items, total_cost = self.process_cart_data(cart_uuids)
#         if cart_items is None:
#             return HttpResponseBadRequest()

#         serializer = CartItemserializer(cart_items, many=True)

#         return Response(status= status.HTTP_201_CREATED)
    
# class GetCartDetail(APIView):
#     def process_cart_data(self, cart_uuids):
#         courses = []
#         cart_cost = Decimal('0.00')

#         for uuid in cart_uuids:
#             item = Course.objects.filter(course_uuid=uuid)

#             if not item:
#                 return None

#             courses.append(item[0])
#             cart_cost += item[0].price

#         return courses, cart_cost

#     def get(self, request):
#         try:
#             body = json.loads(request.body)
#         except json.decoder.JSONDecodeError:
#             return HttpResponseBadRequest()

#         if type(body.get('cart')) != list:
#             return HttpResponseBadRequest()

#         cart_uuids = body.get("cart")
#         if len(cart_uuids) == 0:
#             return Response(data=[])

#         cart_items, total_cost = self.process_cart_data(cart_uuids)
#         if cart_items is None:
#             return HttpResponseBadRequest()

#         serializer = CartItemserializer(cart_items, many=True)

#         return Response({
#             "cart_detail": serializer.data,
#             "cart_total": str(total_cost)
#         })
    

#Access to purchased courses:
class CourseStudy(APIView):
    # permission_classes=[IsAuthenticated]
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
    
#Add to cart:
# class GetCartDetail(APIView):
#     def get_serilizer_class(self):
#         queryset = Cart.objects.all()
#         serializer_class = CartItemserializer


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
            serializer.data, 
            status=status.HTTP_201_CREATED
            )
    
# class CartAPI(APIView):
#     """
#     Single API to handle cart operations
#     """
#     def get(self, request, format=None):
#         cart = Cart(request)

#         return Response(
#             {"data": list(cart.__iter__()), 
#             "cart_total_price": cart.get_total_price()},
#             status=status.HTTP_200_OK
#             )

#     def post(self, request, **kwargs):
#         cart = Cart(request)

#         if "remove" in request.data:
#             product = request.data["products"]
#             cart.remove(product)

#         elif "clear" in request.data:
#             cart.clear()

#         else:
#             product = request.data
#             cart.add(
#                     product=product["products"],
#                     quantity=product["quantity"],
#                     overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
#                 )

#         return Response(
#             {"message": "cart updated"},
#             status=status.HTTP_202_ACCEPTED)