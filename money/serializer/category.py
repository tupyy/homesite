from rest_framework import serializers

from money.models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    id = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        if self.__get_category_name() is not None:
            category = Category.objects.filter(name__exact=self.__get_category_name())
            if len(category) == 0:
                raise serializers.ValidationError('Category ' + self.__get_category_name() + ' is not found')
            (obj, created) = Subcategory.objects.get_or_create(category=category[0], name=validated_data['name'],
                                                               description=validated_data['description'])
            return obj
        else:
            raise serializers.ValidationError('Category not found')

    def update(self, instance, validated_data):
        """
        Update and return an existing Subcategory instance
        :param instance:
        :type instance Subcategory
        :param validated_data:
        :return:
        """

        if self.__get_category_name() is not None:
            category = Category.objects.filter(name__exact=self.__get_category_name())
            if len(category) > 0:
                if category[0].name != instance.category.name:
                    instance.category = category[0]
            else:
                raise serializers.ValidationError("New category not found")

            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance

    class Meta:
        model = Subcategory
        fields = ('id', 'category', 'name', 'description')

    def __get_category_name(self):
        try:
            return self.initial_data['category']
        except KeyError:
            return None


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category
    """
    subcategories = SubcategorySerializer(read_only=True, many=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        (obj, created) = Category.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """
        Update and return an existing Category instance
        :param instance:
        :type instance Category
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'subcategories')
