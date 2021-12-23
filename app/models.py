from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields.related import ForeignKey, ManyToManyField
# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length = 50)

    def caption_name(self):
        return f"{self.caption}"
    
    def __str__(self):
        return self.caption_name()

class Author(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "images")
    slug = models.SlugField(unique = True, max_length = 50)
    date = models.DateField(auto_now_add=True)
    content = models.TextField(validators = [MinLengthValidator(10)])
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    user_name = models.CharField(max_length = 100)
    user_email = models.EmailField()
    text = models.TextField(max_length = 500)
    Date = models.DateField(auto_now_add=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True)


    def __str__(self):
        return f"{self.user_name} {self.user_email}"  # password: h_blog admin panel.