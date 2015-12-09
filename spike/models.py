from django.db import models


class DataPoint(models.Model):
    filed_date = models.DateField()
    drug_name = models.CharField(max_length=200)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "{} Filed on {}: {} = {}".format(self.id, self.filed_date, self.drug_name, self.count)


class DataRecord(models.Model):
    captured_date = models.DateField()
    raw_data = models.CharField(max_length=50000)
    data_src = models.CharField(max_length=30)
    submitted_date = models.DateField()
    def json(self):
        return {
            'captured_date': self.captured_date,
            'raw_data': self.raw_data,
            'data_src': self.data_src,
            'submitted_date': self.submitted_date
        }