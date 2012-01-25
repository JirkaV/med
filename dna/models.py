from django.db import models

UL54_REFERENCE = 'ATGTTTTTCAACCCGTATCTGAGCGGCGGCTTGACCGGCGGTGCGGTCGCGGGTGGCCGGCGTCAGCGTTCGCAGCCCGGATCCGCGCAGGGCTCGGGCAAGCGGCCGCCACAGAAACAGTTTTTGCAGATCGTGCCGCGAGGCGTCATGTTCGACGGTCAGACGGGGTTGATCAAGCATAAGACGGGACGGCTGCCTCTCATGTTCTATCGAGAGATTAAACATTTGTTGAGTCATGACATGGTTTGGCCGTGTCCTTGGCGCGAGACCCTGGTGGGTCGCGTGGTGGGACCTATTCGTTTTCACACCTACGATCAGACGGACGCCGTGCTCTTCTTCGACTCGCCCGAAAACGTGTCGCCGCGCTATCGTCAGCATCTGGTGCCTTCGGGGAACGTGTTGCGTTTCTTCGGGGCCACAGAACACGGCTACAGTATCTGCGTCAACGTTTTCGGGCAGCGCAGCTACTTTTACTGTGAGTACAGCGACACCGATAGGCTGCGTGAGGTCATTGCCAGCGTGGGCGAACTAGTGCCCGAACCGCGGACGCCATACGCCGTGTCTGTCACGCCGGCCACCAAGACCTCCATCTACGGGTACGGGACGCGACCCGTGCCCGATTTGCAGTGTGTGTCTATCAGCAACTGGACCATGGCCAGAAAAATCGGCGAGTATCTGCTGGAGCAGGGTTTTCCCGTGTACGAGGTCCGTGTGGATCCGCTGACGCGTTTGGTCATCGATCGGCGGATCACCACGTTCGGCTGGTGCTCCGTGAATCGTTACGACTGGCGGCAGCAGGGTCGCGCGTCGACTTGTGATATCGAGGTCGACTGCGATGTCTCTGACCTGGTGGCCGTGCCCGACGACAGCTCGTGGCCGCGCTATCGATGCCTGTCCTTCGATATCGAGTGCATGAGCGGCGAGGGTGGTTTTCCCTGCGCCGAGAAGTCCGATGACATTGTCATTCAGATCTCGTGCGTGTGCTACGAGACGGGGGGAAACACCGCCGTGGATCAGGGGATCCCAAACGGGAACGATGGTCGGGGCTGCACTTCGGAGGGTGTGATCTTTGGGCACTCGGGTCTCCATCTCTTTACGATCGGCACCTGCGGGCAGGTGGGCCCAGACGTGGACGTCTACGAGTTCCCTTCCGAATACGAGCTGCTGCTGGGCTTTATGCTTTTCTTTCAACGGTACGCGCCGGCCTTTGTGACCGGTTACAACATCAACTCTTTTGACTTGAAGTACATCCTCACGCGCCTCGAGTACCTGTATAAGGTGGACTCGCAGCGCTTCTGCAAGTTGCCCACGGCGCAGGGCGGCCGTTTCTTTTTACACAGCCCCGCTGTGGGTTTTAAGCGGCAGTACGCCGCCGCCTTTCCCTCGGCTTCTCACAACAATCCGGCTAGCACGGCCGCCACCAAGGTGTATATTGCGGGTTCGGTGGTTATCGACATGTACCCCGTATGCATGGCCAAGACTAACTCGCCCAACTATAAGCTCAACACTATGGCCGAGCTTTACCTGCGGCAACGCAAGGATGACCTGTCCTACAAGGACATCCCGCGTTGTTTCGTGGCTAATGCCGAGGGCCGCGCCCAGGTAGGCCGTTACTGTCTGCAGGACGCCGTATTGGTGCGCGATCTGTTCAACACCATTAATTTTCACTACGAGGCCGGGGCCATCGCGCGGCTGGCTAAAATTCCGTTGCGGCGTGTCATCTTTGACGGACATCAGATCCGTATCTACACCTCGCTGCTGGACGAGTGCGCCTGCCGCGATTTTATCCTGCCCAACCACTACAGCAAAGGTACGACGGTGCCCGAAACGAATAGCGTTGCCGTGTCACCTAACGCTGCTATCATCTCTACCGCCGCTGTGCCCGGCGACGCGGGTTCTGTGGCGGCCATGTTTCAGATGTCGCCGCCCTTACAATCTGCGCCGTCGAGTCAGGACGGCGTTTTACCCGGCTCTGGCAGTAACAGTAGTAGCAGCGTTGGCGTTTTCAGCGTCGGCTCCGGCAGTAGTGGCGGCGTCGGCGTTTCCAACGACAGTCACGGCGCCGGCGGTACTGCGGCGGTTTCGTACCAGGGTGCCACGGTGTTTGAGCCCGAGGTGGGTTATTACAACGACCCCGTGGCCGTGTTCGACTTTGCCAGCCTCTACCCTTCCATCATCATGGCCCACAACCTCTGCTACTCCACCCTGCTGGTGCCGGGTGGCGAGTACCCCGTGGACCCCGCCGACGTATACAGCGTCACGCTAGAGAACGGCGTGACTCACCGCTTTGTGCGTGCTTCGGTGCGCGTCTCGGTGCTTTCGGAACTGCTCAACAAGTGGGTTTCGCAGCGCCGTGCCGTGCGCGAATGCATGCGCGAGTGTCAAGACCCCGTGCGCCGTATGCTGCTCGACAAGGAACAGATGGCACTCAAAGTAACGTGTAACGCTTTCTACGGTTTTACCGGCGTGGTCAACGGCATGATGCCGTGTCTGCCCATCGCCGCCAGCATCACGCGCATCGGTCGCGACATGCTAGAGCGCACGGCGCGGTTCATCAAAGACAACTTTTCAGAGCCGTGTTTTTTGCACAATTTTTTTAATCAGGAAGACTATGTAGTGAGAACGCGGGAGGGGGATTCGGAGGAGAGCAGCACGTTACCGGAGGGGCTCGAAACATCGTCAGGGGGCTCGGACGAACGGCGGGTGGAGGCGCGGGTCATCTACGGGGACACGGACAGCGTGTTTGTCCGCTTTCGTGGCCTGACGCCGCAGGCTCTGGTGGCGCGTGGGCCCAGCCTGGCGCACTACGTGACGGCCTGTCTTTTTGTGGAGCCCGTCAAGCTGGAGTTTGAAAAGGTCTTCGTCTCTCTCATGATGATCTGCAAAAAACGTTACATCGGCAAAGTGGAGGGCGCCTCGGGTCTGAGCATGAAGGGCGTGGATCTGGTGCGCAAGACGGCCTGCGAGTTCGTCAAGGGCGTCACGCGTGACGTCCTCTCGCTGCTCTTTGAGGATCGCGAGGTCTCGGAAGCAGCCGTGCGCCTGTCGCGCCTCTCACTCGATGAAGTCAAGAAATATGGCGTGCCACGCGGTTTCTGGCGTATCTTGCGCCGCCTGGTGCAGGCCCGCGACGATCTGTACCTGCACCGTGTGCGTGTCGAGGACCTGGTGCTTTCGTCGGTGCTTTCTAAGGACATCTCGTTGTACCGTCAATCTAACCTGCCGCACATTGCCGTCATTAAGCGACTGGCGGCCCGTTCTGAGGAGCTACCCTCGGTCGGGGATCGGGTCTTTTACGTCCTGACGGCGCCCGGTGTCCGGACGGCGCCGCAGGGTTCCTCCGACAACGGTGATTCTGTAACCGCCGGCGTGGTTTCCCGGTCGGACGCGATTGATGGCACGGACGACGACGCTGACGGCGGCGGGGTAGAGGAGAGCAACAGGAGAGGAGGAGAGCCGGCAAAGAAGAGGGCGCGGAAACCACCGTCGGCCGTGTGCAACTACGAGGTAGCCGAAGATCCGAGCTACGTGCGCGAGCACGGCGTGCCCATTCACGCCGACAAGTACTTTGAGCAGGTTCTCAAGGCTGTAACCAACGTGCTGTCGCCCGTCTTTCCCGGCGGCGAAACCGCGCGCAAGGACAAGTTTTTGCACATGGTGCTGCCGCGGCGCTTGCACTTGGAGCCGGCTTTTCTGCCGTACAGTGTCAAGGCGCACGAATGCTGTTGA'
UL97_REFERENCE = 'ATGTCCTCCGCACTTCGGTCTCGGGCTCGCTCGGCCTCGCTCGGAACGACGACTCAGGGCTGGGATCCGCCGCCATTGCGTCGTCCCAGCAGGGCGCGCCGGCGCCAGTGGATGCGCGAAGCTGCGCAGGCCGCCGCTCAAGCCGCGGTACAGGCCGCGCAGGCCGCCGCCGCTCAAGTTGCCCAGGCTCACGTCGATGAAGACGAGGTCGTGGATCTGATGACCGACGAGGCCGGCGGCGGCGTCACCACTTTGACCACCCTGAGTTCCGTCAGCACAACCACCGTGCTTGGACACGCGACTTTTTCCGCATGCGTTCGAAGTGACGTGATGCGTGACGGAGAAAAAGAGGACGCGGCTTCGGACAAGGAGAACCAGCGTCGGCCCGTGGTGCCGTCCACGTCGTCTCGCGGCAGCGCCGCCAGCGGCGACGGTTACCACGGCTTGCGCTGCCGCGAAACCTCGGCCATGTGGTCGTTCGAGTACGATCGCGACGGCGACGTGACCAGCGTACGCCGCGCTCTCTTCACCGGCGGCAGCGACCCCTCGGACAGCGTGAGCGGCGTCCGCGGTGGACGCAAACGCCCGTTGCGTCCGCCGTTGGTGTCGCTGGCCCGCACCCCGCTGTGCCGACGTCGTGTGGGCGGCGTGGACGCGGTGCTCGAAGAAAACGACGTGGAGCTGCGCGCGGAAAGTCAGGACAGCGCCGTGGCATCGGGCCCGGGCCGCGTTCCGCAGCCGCTCAGCGGTAGTTCCGGGGAGGAATCCGCCACGGCGGTGGAGGCCGACTCCACGTCACACGACGACGTGCATTGCACCTGTTCCAACGACCAGATCATCACCACGTCCATCCGCGGCCTTACGTGCGACCCGCGTATGTTCTTGCGCCTTACGCATCCCGAGCTCTGCGAGCTCTCTATCTCCTACCTGCTGGTCTACGTGCCCAAAGAGGACGATTTTTGCCACAAGATCTGTTATGCCGTGGACATGAGCGACGAGAGCTACCGCCTGGGCCAGGGCTCCTTCGGCGAGGTCTGGCCGCTCGATCGCTATCGCGTGGTCAAGGTGGCGCGTAAGCACAGCGAGACGGTGCTCACGGTCTGGATGTCGGGCCTGATCCGCACGCGCGCCGCTGGCGAGCAACAGCAGCCGCCGTCGCTGGTGGGCACGGGCGTGCACCGCGGTCTGCTCACGGCCACGGGCTGCTGTCTGCTGCACAACGTCACGGTACATCGACGTTTCCACACAGACATGTTTCATCACGACCAGTGGAAGCTGGCGTGCATCGACAGCTACCGACGTGCCTTTTGCACGTTGGCCGACGCTATCAAATTTCTCAATCACCAGTGTCGTGTATGCCACTTTGATATTACACCCATGAACGTGCTCATCGACGTGAACCCGCACAACCCCAGCGAGATCGTGCGCGCCGCGCTGTGCGATTACAGCCTCAGCGAGCCCTATCCGGATTACAACGAGCGCTGTGTGGCCGTCTTTCAGGAGACGGGCACGGCGCGCCGCATCCCCAACTGCTCGCACCGTCTGCGCGAATGTTACCACCCTGCTTTCCGACCCATGCCGCTGCAGAAGCTGCTCATCTGCGACCCGCACGCGCGTTTCCCCGTAGCCGGCCTACGGCGTTATTGCATGTCGGAGTTGTCGGCGCTGGGTAACGTGCTGGGCTTTTGCCTCATGCGGCTGTTGGACCGGCGCGGTCTGGACGAGGTGCGCATGGGTACGGAGGCGTTGCTCTTTAAGCACGCCGGCGCGGCCTGCCGCGCGTTGGAGAACGGCAAGCTCACGCACTGCTCCGACGCCTGTCTGCTCATTCTGGCGGCGCAAATGAGCTACGGCGCCTGTCTCCTGGGCGAGCATGGCGCCGCGCTGGTGTCGCACACGCTACGCTTTGTGGAGGCCAAGATGTCCTCGTGTCGCGTACGCGCCTTTCGCCGCTTCTACCACGAATGCTCGCAGACCATGCTGCACGAATACGTCAGAAAGAACGTGGAGCGTCTGTTGGCCACGAGCGACGGGCTGTATTTATATAACGCCTTTCGGCGCACCACCAGCATAATCTGCGAGGAGGACCTTGACGGTGACTGCCGTCAACTGTTCCCCGAGTAA'

class ReferenceDNA(models.Model):
    name = models.CharField(max_length=40)
    dna = models.TextField()

    def __unicode__(self):
        return self.name

# fill the database with initial data

#ReferenceDNA.objects.get_or_create(name='UL54', dna=UL54_REFERENCE)
#ReferenceDNA.objects.get_or_create(name='UL97', dna=UL97_REFERENCE)
