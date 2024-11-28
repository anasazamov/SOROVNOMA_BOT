from django.db import models

# Create your models here.

class BotAdmin(models.Model):

    chat_id = models.BigIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Bot(models.Model):

    name = models.CharField(max_length=50)
    token = models.CharField(max_length=100)
    bot_admin = models.ForeignKey(to=BotAdmin,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.token

class Voter(models.Model):

    chat_id = models.BigIntegerField()
    first_name = models.CharField(max_length=1050, blank=True)
    username = models.CharField(max_length=50)
    bot = models.ForeignKey(to=Bot,on_delete=models.CASCADE)

class REQUIRED_CHANNELS(models.Model):

    channel = models.CharField(max_length=50)
    username = models.CharField(max_length=50, blank= True)
    channel_link = models.URLField(max_length=150, blank= True)
    channel_id = models.IntegerField(blank= True,null=True)
    bot = models.ForeignKey(to=Bot,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.channel
    
class Options(models.Model):

    option = models.CharField(max_length=50)
    total_vote = models.IntegerField(default=0)
    votes = models.ManyToManyField(Voter)

    def __str__(self) -> str:
        return self.option

class Question(models.Model):

    name = models.TextField()
    option = models.ManyToManyField(Options)
    bot = models.ForeignKey(to=Bot,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    voter = models.ManyToManyField(Voter)

    def __str__(self) -> str:
        return self.name

    