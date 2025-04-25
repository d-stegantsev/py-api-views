from rest_framework import serializers

from cinema.models import Movie, Actor, Genre, CinemaHall


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    actors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all()
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )
    duration = serializers.IntegerField()

    def create(self, validated_data):
        actors = validated_data.pop("actors")
        genres = validated_data.pop("genres")
        movie = Movie.objects.create(**validated_data)
        movie.actors.set(actors)
        movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description",
            instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)

        if "actors" in validated_data:
            instance.actors.set(validated_data["actors"])

        if "genres" in validated_data:
            instance.genres.set(validated_data["genres"])

        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class CinemaHallSerializer(serializers.ModelSerializer):
    rows = serializers.IntegerField(min_value=1)
    seats_in_row = serializers.IntegerField(min_value=1)

    class Meta:
        model = CinemaHall
        fields = "__all__"
