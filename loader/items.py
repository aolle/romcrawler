from scrapy.item import Item, Field  

class RomItem(Item):  
	platform = Field()
	title = Field()   
	size = Field()
	url = Field()
	letter = Field()
	pass

