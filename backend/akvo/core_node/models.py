from django.db import models

# Create your models here.


class Node(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "node"


class NodeDetail(models.Model):
    node = models.ForeignKey(
        to=Node,
        on_delete=models.CASCADE,
        related_name="node_details"
    )
    code = models.CharField(max_length=255)
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "node_detail"
