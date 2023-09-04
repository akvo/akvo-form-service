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
        to=Node, on_delete=models.CASCADE, related_name="node_details"
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    code = models.CharField(
        max_length=255,
        null=True,
    )
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "node_detail"
