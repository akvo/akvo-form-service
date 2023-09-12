from django.core.management import BaseCommand
from akvo.core_node.models import Node
from akvo.utils.custom_generator import generate_sqlite


class Command(BaseCommand):

    def handle(self, *args, **options):
        nodes = Node.objects.all()
        for node in nodes:
            generate_sqlite(node=node)
