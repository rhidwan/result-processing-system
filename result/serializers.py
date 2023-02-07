from rest_framework import serializers

from user.serializers import UserSerializer

from .models import ExamMark, Score

class ExamMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamMark
        # fields = '__all__'
        exclude= ('course',)

class ScoreSerializer(serializers.ModelSerializer): 
    approved_by = UserSerializer(many=True)# this will return a list
    section_a = ExamMarkSerializer()
    section_b = ExamMarkSerializer()

    class Meta:
        model = Score
        exclude = ('is_improvement', 'previous_score', 'id', 'course', 'student', 'catm', 'is_improved' )
        # read_only_fields = ('id', 'data', 'roll_no')
        depth = 1
    