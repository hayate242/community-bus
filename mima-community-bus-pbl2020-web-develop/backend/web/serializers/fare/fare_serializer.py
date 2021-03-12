from rest_framework import serializers

from bus.models import MasterFares


class FareSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterFares
        fields = "group", "amount"

    def create(self, validated_data):
        print(validated_data)
        self.Meta.model.objects.alive()\
            .exclude(amount=0)\
            .get(group=validated_data["group"]).delete()
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["amount"] = f"{instance.amount}"
        return representation
