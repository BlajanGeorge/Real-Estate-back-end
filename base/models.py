from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
class ValidCountry(models.TextChoices):
	ROMANIA = 'Romania'
	USA = 'USA'
	GERMANY = 'Germany'
	FRANCE = 'France'
	ITALY = 'Italy'
	BRAZIL = 'Brazil'

class ValidCity(models.TextChoices):
	BUCUREST = 'Bucuresti', 'Romania'
	CLUJ = 'Cluj-Napoca', 'Romania'
	BRASOV = 'Brasov', 'Romania'
	CONSTANTA = 'Constanta', 'Romania'
	TIMISOARA = 'Timisoara', 'Romania'
	NEW_YORK = 'New York', 'USA'
	LOS_ANGELES = 'Los Angeles', 'USA' 
	CHICAGO = 'Chicago', 'USA'
	MUNICH = 'Munich', 'Germany'
	BERLIN = 'Berlin' , 'Germany'
	FRANKFURT = 'Frankfurt', 'Germany'
	PARIS = 'Paris', 'France'
	LYON = 'Lyon', 'France'
	ROMA = 'Roma', 'Italy'
	NAPOLI = 'Napoli', 'Italy'
	SAO_PAULO = 'Sao Paulo', 'Brazil'
	RIO_DE_JANEIRO = 'Rio de Janeiro', 'Brazil'

class Role(models.TextChoices):
	AGENT = 'AGENT'
	CUSTOMER = 'CUSTOMER'

class Exchange(models.TextChoices):
	EURO = 'Euro'
	DOLLAR = 'Dollar'
	POUND = 'Pound'

class PropertyType(models.TextChoices):
	HOUSE = 'House'
	APARTMENT = 'Apartment'

class Property(models.Model):
	country = models.CharField(max_length=100, choices = ValidCountry.choices)
	city = models.CharField(max_length=100, choices = ValidCity.choices)
	address = models.CharField(max_length=300, blank=False)
	exchange = models.CharField(max_length=30, choices = Exchange.choices)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(900000000.00)])
	square_feet = models.PositiveSmallIntegerField(validators = [MaxValueValidator(1000), MinValueValidator(10)])
	rooms = models.PositiveSmallIntegerField(validators = [MaxValueValidator(30), MinValueValidator(1)])
	type = models.CharField(max_length=20, choices = PropertyType.choices)
	class Meta:
		db_table='property'

class PropertyPhoto(models.Model):
	url = models.CharField(max_length=200, default=None)
	property = models.ForeignKey(Property, on_delete=models.CASCADE, default=None)
	class Meta:
		db_table='property_photo'

class User(models.Model):
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank=False)
	address = models.CharField(max_length=300, blank=False)
	phone = models.CharField(max_length=100, blank=False)
	email = models.CharField(max_length=350, blank=False, unique=True, validators=[RegexValidator("^[\\w!#$%&'*+/=?`{|}~^-]+(?:\\.[\\w!#$%&'*+/=?`{|}~^-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,6}$", "Invalid email format")])
	password= models.CharField(max_length=100, blank=False, validators=[RegexValidator("^(?=.*[0-9])"
      + "(?=.*[a-z])(?=.*[A-Z])"
      + "(?=.*[@#$%^&+=])"
      + "(?=\\S+$).{8,20}$","Invalid password format")])
	country = models.CharField(max_length=100, choices = ValidCountry.choices)
	city = models.CharField(max_length=100, choices = ValidCity.choices)
	role = models.CharField(max_length=50, choices = Role.choices)
	favorites = models.ManyToManyField(Property)

	class Meta:
		db_table='user'

