from django.db import models
from apis.models.competition import Competition


class CompetitionImage(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='competitions/images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.competition.title}"
    
    
    def save(self, *args, **kwargs):
     if self.is_main:
        CompetitionImage.objects.filter(
            competition=self.competition, is_main=True
        ).update(is_main=False)
     super().save(*args, **kwargs)