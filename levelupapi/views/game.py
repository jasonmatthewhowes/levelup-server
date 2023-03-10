"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models import Gamer
from levelupapi.models import GameType


class GameView(ViewSet):
    """Level up view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single
        
        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
    
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            name=request.data["name"],
            gamer=gamer,
            game_type=game_type,
            description=request.data["description"],
            maker=request.data["maker"],
            skill_level=request.data["skill_level"],
            number_of_players=request.data["number_of_players"],
            
            
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=201)

    def update(self, request, pk):
    #handles put request
        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.maker = request.data["maker"]
        game.description = request.data["description"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        gamer = Gamer.objects.get(pk=request.data["gamer"])
        game.gamer = gamer
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer 
    """
    class Meta:
        model = Game
        fields = ('id', 'name', 'gamer', 'game_type', 'description','maker', 'skill_level', 'number_of_players')



