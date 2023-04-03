from rest_framework import serializers
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from . models import Perk
from . models import Experience
from wishlists.models import Wishlist


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )
    reviews = ReviewSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "description",
            "country",
            "city",
            "address",
            "rating",
            "price",
            "is_liked",
            "is_host",
            "host",
            "category",
            "perks",
            "reviews",
            "created_at",
            "updated_at",
        )

    def get_rating(self, experience):
        return experience.average_ratings()

    def get_is_host(self, experience):
        return experience.host == self.context["request"].user
    
    def get_is_liked(self, experience):
        return Wishlist.objects.filter(user=self.context["request"].user, 
                                       experiences__pk = experience.pk).exists()