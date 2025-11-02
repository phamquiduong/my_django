from rest_framework import serializers

from account.models import Ward


class WardSerializer(serializers.ModelSerializer):
    province = serializers.HyperlinkedRelatedField(view_name="account_provinces_api-detail", read_only=True)

    class Meta:
        model = Ward
        fields = "__all__"
