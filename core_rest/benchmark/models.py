from django.db import models
from submission.models import Submission


class Benchmark(models.Model):
    submission_id = models.ForeignKey(Submission, on_delete=models.CASCADE, null=False, blank=False,
                                      verbose_name='submission_id')
    correctness = models.BooleanField(default=False, blank=False, null=False, verbose_name='correctness')
    completeness = models.BooleanField(default=False, blank=False, null=False, verbose_name='completeness')
    time_complexity = models.CharField(default='N/A', blank=False, null=False, verbose_name='time_complexity',
                                       max_length=10)
    space_complexity = models.CharField(default='N/A', blank=False, null=False, verbose_name='space_complexity',
                                        max_length=10)
    cprofile = models.TextField(default='N/A', blank=False, null=False, verbose_name='cprofile')
    score = models.FloatField(default=0.0, blank=False, null=False, verbose_name='score')

    def serialized(self):
        data = {
            'id': self.id,
            'submission': self.submission_id.serialized(),
            'correctness': self.correctness,
            'completeness': self.completeness,
            'time_complexity': self.time_complexity,
            'space_complexity': self.space_complexity,
            'cprofile': self.cprofile,
            'score': self.score
        }
        return data
