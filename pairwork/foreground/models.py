from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    #fixed
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    updater = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        abstract = True

class Profile(BaseModel):
	user = models.ForeignKey(User, unique=True)
	nickname = models.CharField(max_length=200)
	gender = models.SmallIntegerField() # 0 is None, 1 is male, 2 is female
	age = models.SmallIntegerField()

	# contacts, should split to a single model?
	gtalk = models.CharField(max_length=50)
	skype = models.CharField(max_length=50)
	qq = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)

class CommonIntentInfo(BaseModel):
	user = models.ForeignKey(User)
	_type = models.CharField(max_length=100) # intent info type, some strong relation like Work time , Work place, Work content, Gender, Age range and some weak relation like Constellation, Color of skin ...
	isStrongRelation = models.BooleanField(default=False) # strong or weak relation.
	weight = models.IntegerField(default=1) # Weights of this info
	misc = models.CharField(max_length=200) # intent info content
