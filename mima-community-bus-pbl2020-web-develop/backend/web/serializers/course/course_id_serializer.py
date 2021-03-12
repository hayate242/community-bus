from rest_framework import serializers

from bus.models import MasterCourse


class CourseIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCourse
        fields = ("id",)
        extra_kwargs = {
            "id": {"read_only": False},
        }


class CourseIdSerializerForDel(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=MasterCourse.objects.alive(),
        source="course"
    )
