from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . models import Perk
from . models import Experience
from categories.models import Category
from . import serializers


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = serializers.PerkSerializer(data = request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(serializers.PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk = pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)
    
    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data = request.data, partial =True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(HTTP_204_NO_CONTENT)


class Experiences(APIView):
    
    def get(self, request):
        experience_all = Experience.objects.all() # django
        serializer = serializers.ExperienceSerializer(experience_all, many=True) # django -> json
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceSerializer(data=request.data) # django
        if serializer.is_valid():
            category_pk = request.data.get("category")
            perk_pks = request.data.get("perks")

            # category control
            if not category_pk:
                raise ParseError("category는 필수입니다.")
            else:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("category는 experience여야 합니다.")
                except Category.DoesNotExist:
                    raise NotFound
            
            # insert transaction
            try:
                with transaction.atomic():
                    new_experience = serializer.save(host=request.user)
                    if perk_pks:
                        for perk_pk in perk_pks:
                            perk = Perk.objects.get(pk=perk_pk)
                            new_experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise NotFound
            except Exception as e:
                raise ParseError(e)

            ex_serializer = serializers.ExperienceSerializer(new_experience) #django -> json
            
            return Response(ex_serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return NotFound
        
    def get(self, request, pk):
        experience = self.get_object(pk)
        return Response(serializers.ExperienceDetailSerializer(experience, context={"request":request}).data)
    
    def put(self, request, pk):
        experience = self.get_object(pk)