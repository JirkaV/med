from django.core.management.base import BaseCommand
from med.dna.models import ReferenceDNA, UL54_REFERENCE, UL97_REFERENCE

class Command(BaseCommand):
    help = 'Puts reference data in the database'

    def handle(self, *args, **options):
        ReferenceDNA.objects.get_or_create(name='UL54', dna=UL54_REFERENCE)
        ReferenceDNA.objects.get_or_create(name='UL97', dna=UL97_REFERENCE)
        return 'Done successfully'
