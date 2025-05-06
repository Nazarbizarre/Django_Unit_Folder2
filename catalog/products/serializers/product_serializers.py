from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name',
                'description',
                'entity',
                'price',
                'available',
                'category',
                'nomenclature',
                'created_at',
                'rating',
                'discount',
                'attributes',
                'discount_price'
                ]

    def get_discount_price(self, obj):
        return obj.discount_price