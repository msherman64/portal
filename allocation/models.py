
from django.contrib.auth.models import Group
from django.db import models

from user.models import ChameleonUser

def _descriptionFileLocation(allocation_request, filename):
    (name, extension) = os.path.splitext(filename)
    return os.path.join(settings.MEDIA_ROOT,"allocation_requests",allocation_requests,"description."+extension)


# Alamo virtual machines, Hotel virtual machines
# Alamo object store?, Hotel object store?
# Alamo bare metal, Hotel bare metal
# etc.
class Resource(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

#class ScienceField(models.CharField):
#    FIELDS = (
#        ("",""),
#    )
#
#    def __init__(self, *args, **kwargs):
#        kwargs["max_length"] = 100
#        kwargs["choices"] = ScienceField.FIELDS
#        models.CharField.__init__(self,*args,**kwargs)

# this is an alternative to ScienceField
class FieldOfScience(models.Model):
    name = models.CharField(max_length=100)
    #parent = models.OneToOneField(FieldOfScience,blank=True)

    def __unicode__(self):
        return self.name

# FutureGrid project process:
#   * create an AllocationRequest for each one
#   * when the PI or allocation manager claims it, create the Group and Allocation

class AllocationRequest(models.Model):
    title = models.CharField(max_length=100)

    # name is only valid when requesting a New allocation
    # name should be a valid Linux group name
    #   at most 16 characters
    #   satisfying: [a-z][0-9a-z\-]*
    # it will become the Group.name
    #   can't be an existing Group name or User name
    name = models.CharField(max_length=100,blank=True,
                            help_text="a short project name - only valid for New allocations")

    abstract = models.TextField(max_length=2000)
    key_words = models.CharField(max_length=200)

    # The PI for a New allocation, the PI or allocation manager for the others
    requester = models.OneToOneField(ChameleonUser,related_name="alloc_req_requester")

    initial_users = models.ManyToManyField(ChameleonUser,related_name="alloc_req_initial_users")

    field_of_science = models.ManyToManyField(FieldOfScience)
    #primary_field_of_science = ScienceField()
    #secondary_field_of_science = ScienceField(blank=True)

    # should grants be a separate Model?
    nsf_grant = models.CharField(max_length=50,
                                 blank=True,
                                 help_text="the NSF grant that will be supported by this allocation")

    # alternative way that stores the fields in the database
    #field_of_science = models.ManyToManyField(FieldOfScience)

    # extension - more duration, no more units
    # supplement - more units, no more duration
    # renewal - more units and duration
    TYPE = (
        ("N","New"),
        ("E","Extension"),
        ("S","Supplement"),
        ("R","Renewal"),
    )
    request_type = models.CharField(max_length=1,choices=TYPE)

    # this shouldn't be needed with Allocation.request
    #allocation = models.OneToOneField(Allocation,blank=True,
    #                                  help_text="existing allocation this request is related to")

    # documents from XSEDE: main document, PI CV, Code performance and scaling
    description = models.FileField(upload_to=_descriptionFileLocation,
                                   blank=True,
                                   help_text="project description - required for allocations over ??? units")
    
    resource = models.ManyToManyField(Resource,help_text="the resources you expect to use")

    units = models.IntegerField(help_text="the number of units requested")
    duration = models.IntegerField(default=12,
                                   help_text="the number of months the allocation will be valid for")

    submit_date = models.DateField()

    review_date = models.DateField()

    STATUS = (
        ("I","Incomplete"),
        ("S","Submitted"),
        ("A","Approved"),
        ("D","Denied"),
    )
    status = models.CharField(max_length=1,choices=STATUS)
    granted_units = models.IntegerField(blank=True,help_text="the number of units granted")
    granted_duration = models.IntegerField(blank=True,
                                           help_text="the number of months granted")

class Allocation(models.Model):
    principal_investigator = models.OneToOneField(ChameleonUser,related_name="allocation_pi")
    allocation_manager = models.OneToOneField(ChameleonUser,blank=True,related_name="allocation_manager",
                                              help_text="an alternate user that can manage this allocation")

    # group.name should be a valid Linux group name
    group = models.OneToOneField(Group)

    join_request = models.ManyToManyField(ChameleonUser, help_text="users that have asked to join this allocation")

    # could be several requests associated with an allocation
    allocation_request = models.ManyToManyField(AllocationRequest)

    start_date = models.DateField()
    end_date = models.DateField()

    granted_amount = models.IntegerField(help_text="the amount of units granted")
    remaining_amount = models.IntegerField(help_text="the amount of units remaining")
