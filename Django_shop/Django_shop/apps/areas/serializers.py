from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id','name')

class SubAreaSerializer(serializers.ModelSerializer):

    subs = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id','name', 'subs')