from users.models import User
from django.db.models import Model, CharField, DateTimeField, ForeignKey, CASCADE, TextField


class Tweet(Model):
    # user = ForeignKey(User, on_delete=CASCADE)
    text = CharField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    owner = ForeignKey('auth.User', related_name='tweets', on_delete=CASCADE)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        super(Tweet, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text


class Comment(Model):
    tweet = ForeignKey(Tweet, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    text = CharField(max_length=200)

    def __str__(self):
        return self.tweet.text


class Like(Model):
    tweet = ForeignKey(Tweet, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.tweet.text
