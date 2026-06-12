from rest_framework import serializers

class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField()

    end = serializers.CharField()

    def validate(self, attrs):
        if attrs["start"] == attrs["end"]:
            raise serializers.ValidationError(
                "[!] Start and end cannot be the same."
            )
        return attrs