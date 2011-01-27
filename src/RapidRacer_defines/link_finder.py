from urllib import FancyURLopener
import re

G_API    = "http://www.google.com/search?"
G_SEARCH = "q="
G_SITE   = "start="

class Finder():
	
	def __init__(self):
		
		self.opener 	 = FancyURLopener()
		self.__content	 = 0
		self.__page 	 = ""
		self.url		 = ""

	def __gen_search_url(self,keyword_list,site):
		
		# Add keywords to the G_API string
		tmp_url = G_API+G_SEARCH

		for e in keyword_list:
			tmp_url = tmp_url+e+"+"
		
		# Overwrite the last "+" in the URL string with a
		# "&"
		tmp_url = tmp_url[0:-1]+"&"

		# Add the site option to the URL string
		tmp_url = tmp_url+G_SITE+site
		return tmp_url

	def google_get_search(self,keyword_list=[],site="0"):

		# Call the self.__gen_search_url method with the given
		# keyword_list as parameter
		self.url = self.__gen_search_url(keyword_list,site)

		# Get data by opening the generated url with an instance
		# of the FancyURLopener
		self.__content = self.opener.open(self.url)
	
	def get_page(self, url):
		
		self.url = url
		self.__content = self.opener.open(self.url)

	def search_any_links_on_site(self,ignored_cont=[]):
		
		# Return 4 if self.__content is empty
		if not self.__content:
			return 4
		# Define some used variables
		content   = self.__content
		link_list = []

		# Get page content and search everything, that looks like a link
		# via regexp
		self.__page = content.read()
		tmp_list = re.findall(r"http://\S*[\",\,]?"[0:-1],self.__page)

		for element in tmp_list:
			
			contains = 0
			
			# Search for unwanted keywords in every URL in the list
			for cont in ignored_cont:
				if cont in element:
					#print "[*] In \"for\" loop"
					contains = 1
					break
			# If no unwanted keywords were found, append the element to
			# the link_list
			if not contains:
				link_list.append(element)
		
		return link_list
	
	def search_rs_links_on_site(self):
		
		# Get page content and search everything, that looks like a 
		# rapidshare link via regexp
		content = self.__content
		self.__page = content.read()
		link_list = (re.findall(r"http://www.rapidshare.com[\w,/,\\,\.]*",self.__page)+
					 re.findall(r"http://rapidshare.com[\w,/,\\,\.]*"    ,self.__page))

		return link_list