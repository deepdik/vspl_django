from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class HomePageImage(models.Model):
	image =  models.ImageField(upload_to ='HomePageImage/',
									)
	def __str__(self):
		return self.image
	class Meta:    
		verbose_name_plural = "Home Page Image"

class City(models.Model):
	city    = models.CharField(max_length=40,unique=True)
   
	def __str__(self):
		return self.city
	class Meta:    
		verbose_name_plural = "City"

class RateList(models.Model):
	city    		= models.OneToOneField(City,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.city.city + ' Rate List'
	class Meta:    
		verbose_name_plural = "Rate List"


class RateOfProduct(models.Model):
	city    		= models.ForeignKey(RateList,on_delete=models.CASCADE)
	product_name 	= models.CharField(max_length=50)
	rate            = models.PositiveIntegerField(help_text='rate of product per kg')        
   
	def __str__(self):
		return self.product_name
	class Meta:    
		verbose_name_plural = "Rate Of Product"

class SellDemand(models.Model):
	customer  		= models.ForeignKey(User ,on_delete=models.DO_NOTHING)
	city  			= models.ForeignKey(City,on_delete=models.DO_NOTHING)
	total_qty  		= models.PositiveIntegerField(blank=True,null=True) 
	totel_price 	= models.PositiveIntegerField(blank=True,null=True)
	free_delivery 	= models.BooleanField('free Delievery eligible',blank=True,null=True)
	created     	= models.DateField(auto_now_add=True) 

	def __str__(self):
		return self.user.first_name + '-' +self.city.city
	class Meta:    
		verbose_name_plural = "Sell Demands"

class ProductListDetail(models.Model):
	sell  	=  models.ForeignKey(SellDemand,on_delete=models.CASCADE)
	name  	=  models.CharField(max_length=50)
	rate  	=  models.PositiveIntegerField()
	qty   	=  models.PositiveIntegerField()
	price 	=  models.PositiveIntegerField()

	def __str__(self):
		return self.name
	class Meta:    
		verbose_name_plural = "Product List Details"

CALL = (('done','Done'),('not done','Not Done'))

class StaffAction(models.Model):
	staff_user  	= models.ForeignKey(User ,on_delete = models.DO_NOTHING)
	sell  			= models.OneToOneField(SellDemand,on_delete = models.CASCADE)
	call_to_cust    = models.CharField('Call with customers',choices=CALL)


	def __str__(self):
		return self.name
	class Meta:    
		verbose_name_plural = "Staff Action"


