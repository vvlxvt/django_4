import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women

class WomenSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # скрываю выбор текущего пользователя, тк он становится автоматически автором
    class Meta:
        model = Women
        fields = '__all__'



    '''
class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=100)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField() # в сериализаторе опеределяется конекретно как целое число а не как внешний ключ
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        return Women.objects.create(**validated_data) # возвращаю объект который был создан

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.content = validated_data.get("content", instance.content)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.save()
        return instance

    def delete(self, instance):
        return instance.delete()
'''







# def encode():
#     model = WomenModel('Sher', 'Content: Sher')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Sher","content":"Content: Sher"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
