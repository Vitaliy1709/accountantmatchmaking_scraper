from django.db import models


class Location(models.Model):

    # Australian_postcodes
    postcode = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, default="New")

    def __str__(self):
        return f"{self.postcode} - {self.city}, {self.state}, {self.status}"



class Company(models.Model):

    # Basic Information
    company_id = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    image_id = models.CharField(max_length=255, null=True, blank=True)
    consultation_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    search_id = models.CharField(max_length=255, unique=True, blank=True)
    distance_from_search_location = models.FloatField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone_numbers = models.JSONField(null=True, blank=True)
    languages = models.JSONField(null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    years_in_business = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="New")

    # Communication with Location
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    # Address Information
    addresses = models.JSONField(null=True, blank=True)

    # Criteria Information
    distance_within = models.FloatField(null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    # Services and Certifications
    services = models.JSONField(null=True, blank=True)
    certifications = models.JSONField(null=True, blank=True)

    # Person Information
    person_name = models.CharField(max_length=255, null=True, blank=True)
    person_family = models.CharField(max_length=255, null=True, blank=True)

    # Expertise Information
    software_expertise = models.JSONField(null=True, blank=True)
    industries = models.JSONField(null=True, blank=True)

    # Reviews Information
    avg_overall_rating = models.FloatField(null=True, blank=True)
    number_of_reviews = models.IntegerField(null=True, blank=True)

    # Professional Designations
    professional_designations = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.person_name} {self.person_family}"

