from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from .models import Wishlist
from .serializers import WishlistSerializer
from rooms.models import Room


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user = request.user)
        serializer = WishlistSerializer(wishlists, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data = request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user = request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, context={'request':request})
        return Response(serializer.data)        

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        ) # user -> django
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            updated_serializer = WishlistSerializer(
                updated_wishlist,
                context={"request": request},
            ) # django -> user
            return Response(updated_serializer.data)
        else:
            return Response(serializer.errors)
            


class WishlistToggle(APIView):
    # API: "<int:pk>/rooms/<int:room_pk>"
    # request -> 있는지 없는지 확인
    # 있으면 삭제/ 없으면 추가

    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room_pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        
        return Response(status=HTTP_200_OK)
