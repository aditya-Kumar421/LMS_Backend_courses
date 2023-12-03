from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Comment, CourseSection, Episode, Cart
from users.serializers import UserSerializer

#change
class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_student')
    author = UserSerializer()
    #change
    image_url=serializers.CharField(source="get_absolute_image_url")

    class Meta:
        model = Course
        fields = ["course_uuid", "title", "student_no", "author", "price","image_url"]
        #:   

class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=Comment
        exclude=[
            'id'
        ]

class EpisodeUnpaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    file=serializers.CharField(source='get_absolute_url')
    class Meta:
        model=Episode
        fields=[
            "title",
            "length",
            "file" 
        ] 

class EpisodePaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    file=serializers.CharField(source='get_absolute_url')
    class Meta:
        model=Episode
        fields=[
            "title",
            "file",
            "length",
        ]

class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes=EpisodeUnpaidSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    class Meta:
        model=CourseSection
        fields=[
            'section_title',
            'episodes',
            'total_duration',
        ]

class CourseSectionPaidSerializer(ModelSerializer):
    episodes=EpisodePaidSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    class Meta:
        model=CourseSection
        fields=[
            'section_title',
            'episodes',
            'total_duration',
        ]
#change
class CourseUnpaidSerializer(ModelSerializer):
    comments=CommentSerializer(many=True)
    author = UserSerializer()
    course_section=CourseSectionUnPaidSerializer(many=True)
    student_no=serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration=serializers.CharField(source='total_course_length')
    image_url=serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model=Course
        exclude=[
            'id'
        ]

class CoursePaidSerializer(ModelSerializer):
    comments=CommentSerializer(many=True)
    author = UserSerializer()
    course_section=CourseSectionPaidSerializer(many=True)
    student_no=serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration=serializers.CharField(source='total_course_length')
    #change
    image_url=serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model=Course
        exclude=[
            'id'
        ]

class CourseListSerailizer(ModelSerializer):
    student_no=serializers.IntegerField(source='get_enrolled_student')
    author=UserSerializer()
    description=serializers.CharField(source='get_brief_description')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    image_url=serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model=Course
        fields =[
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
            'description',
            'total_lectures'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude=['id']


