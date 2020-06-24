# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 21:47:34 2020

@author: Dulanjaya
"""

import scrapy
import json 
import re


class ScrapeData(scrapy.Spider):
    name = "scrape_data"
    objects = []
    allowed_domains= [
        'sinhalasongbook.com'
        ]

    
    def start_requests(self):
        urls = [
        ]
        for i in range(1,23):
            
            urls.append('https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page='+str(i))
            
        print(urls)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    

    def parse(self, response):

        for quote in response.xpath('/html/body/div[1]/div[1]/div/main/article/div/div[3]/div[1]/div/div/div/h4/a/@href').getall():
            
            yield scrapy.Request(quote, callback=self.details_extractor)
            
            
    def details_extractor(self, response):
        
        details= {
            'artist' : " , ".join(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[2]/div/div/ul/li[1]/span/a/text()').getall()).strip(),
            'genere' : " , ".join(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[2]/div/div/ul/li[2]/span/a/text()').getall()).strip(),         
            'lyrics by' :" , ".join(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[1]/span/a/text()').getall()).strip(),
            'music' : " , ".join(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[2]/span/a/text()').getall()).strip(),
            'movie' :" , ".join(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[3]/span/a/text()').getall()).strip(),
            'name' : response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/h2/span/text()').get().strip(),
            'views' : response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div/text()').getall()[-1].split('-')[-1].split("Visits")[0].strip(),
            'shares' : response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div/div[4]/span/text()').get(),
            'lyrics' : 
                #response.xpath('//pre/text()').getall()
                re.sub("[-+a-zA-Z0-9#|\/()\t{}∆—]",""," ".join( response.xpath('//pre/text()').getall())).strip().replace("  ", "")
            }
#        print(response.xpath('//pre/text()').getall())
        self.objects.append(details)
        with open("lyrics_objects.json", 'w', encoding="utf8") as outfile:
           json.dump(self.objects, outfile,indent = 4, sort_keys=True)
        
    def closed(self, reason):
        
        with open("lyrics_objects.json", 'w', encoding="utf8") as outfile:
           json.dump(self.objects, outfile,indent = 4,ensure_ascii=False)
           

        
        
