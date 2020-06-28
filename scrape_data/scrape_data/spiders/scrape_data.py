# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 21:47:34 2020

@author: Dulanjaya
"""

import scrapy
import json 
import re
from googletrans import Translator


class ScrapeData(scrapy.Spider):
    name = "scrape_data"
    artist_name_translator = Translator()
    genere_name_translator = Translator()
    lyrics_by_name_translator = Translator()
    music_by_name_translator = Translator()
    movie_tranlator = Translator()
    objects = []
    song_name=""
    artist_name=""
    genere_name=""
    lyrics_by_name=""
    music_by_name=""
    lyrics=""
    key=""
    word_dic={
        "Premasiri Khemadasa":"ප්‍රේමසිරි කේමදාස",
        "Upali Dhanawalawithana":"උපාලි ධනවලවිතාන",
        "Kularathna Ariyawansa":"කුලරත්න ආරියවංශ",
        "Rohana Weerasingha":"රෝහණ වීරසිංහ",
        "Anoma Rasaputhra":"අනෝමා රාසපුත්‍ර",
        "Annesley Malawana":"ඇනස්ලි මාලේවන",
        "Patrick Denipitya":"පැට්රික් දෙනිපිටිය",
        "Chandralekha Perera":"චන්ද්‍රලේඛා පෙරේරා",
        "Ajith Bandara":"අජිත් බණ්ඩාර",
        "Rohana Jayasinghe":"රෝහණ ජයසිංහ",
        "Athma Liyanage":"ආත්මා ලියනගේ",
        "Dharma Sri Wickramasingha":"ධර්ම ශ්‍රී වික්‍රමසිංහ",
        "C.T.Perera":"සී.ටී.පෙරේරා",
        "Lushan Bulathsinhala":"ලුෂන් බුලත්සිංහල",
        "Benadict Fernando":"බෙනඩික් ප්‍රනාන්දු",
        "Angelin Gunathilaka":"ඇන්ජලීන් ගුණතිලක",
        "Hemasiri Halpita":"හේමසිරි හල්පිට",
        "Nanda Malani":"නන්දා මාලනී",
        "Inspirational":"උද්වේගකර",
        "Buddhadasa Galappaththi":"බුද්ධදාස ගලප්පත්ති",
        "Karunaratna Divulgane":" කරුණාරත්න දිවුල්ගනේ",
        "Chithra Vakishta":"චිත්‍රා වාකිෂ්ඨ",
        "B Nanayakkarawasam":"බී නානායක්කාරවසම්",
        "Stanley Pieris":"ස්ටැන්ලි පීරිස්",
        "Somathilaka Jayamaha":"සෝමතිලක ජයමහ",
        "Bandula Nanayakkarawasam":"බන්දුල නානායක්කාරවසම්",
        "Milton Mallawarachchi":"මිල්ටන් මල්ලවාරච්චි",
        "Kasun Kalhara":"කසුන් කල්හාර",
        "Yamuna Malani Perera":"යමුනා මාලනී පෙරේරා",
        "Wijesiri Amaratunga":"විජේසිරි අමරතුංග",
        "Punyasiri Mahawaththa":"පුන්යසිරි මහවත්ත",
        "Sarath Wimalaweera":"සරත් විමලවීර",
        "Kushani Sandarekha":"කුෂානි සඳාරේඛා",
        "George Palliawaththa":"ජෝර්ජ් පල්ලයවත්ත",
        "Rambukkana Siddhartha Thero":"රම්බුක්කන සිද්ධාර්ථ හිමි",
        "K.A.W.Perera":"කේ.ඒ.ඩබ්ලිව්.පෙරෙරා",
        "Kularathna Ariyawans":"කුලරත්න ආරියවන්ශ",
        "Kumari Lanka":"කුමාරි ලංකා",
        "Dishan Nanayakkara":"දිෂාන් නානායක්කාර",
        "Narada Disasekara": "නාරද දිසාසේකර",
        "Sunil Dayananda Konara":"සුනිල් දයානන්ද කෝනාර",
        "Kusum Pieris":"කුසුම් පීරිස්",
        "Rachita Wakishta":"රචිතා වාකිෂ්ඨ",
        "Thilina Ruhunuge" : "තිලිණ රුහුණගේ",
        "Saman Athawudahetti":"සමන් අතාවුදහෙට්ටි",
        "Dayarathna Ranatunga":"දායාරත්න රණතුංග",
        "Bandara Athauda":"බන්ඩාර අතාවුද",
        "Romles Perera":"රොම්ල්ස් පෙරේරා",
        "Nimal Ananada":"නිමල් ආනන්ද",
        "Jayathissa Alahakoon":"ජයතිස්ස අලහකෝන්",
        "Ruchira Paranawitharana":"රුචිරා පරණවිතාරණ",
        "Praneeth Abayasundara":"ප්‍රනීත් අබේසුන්දර",
        "Sisira Senarathna":"සිසිර සේනාරත්න",
        "Kalum Shreemal":"කැළුම් ශ්‍රීමාල්",
        "Wimala R Pieris":"විමලා ආර් පීරිස්",
        "Ranjani Perera":"රංජනි පෙරේරා",
        "Chandrasena Range":"චන්ද්‍රසේන රන්ගෙ",
        "Mahesh Denipitiya":"මහේෂ් දෙනිපිටිය",
        "Ananda Samarakoon":"ආනන්ද  සමරකෝන්",
        "Dayarathna Ranathunga":"දයාරත්න රණතුංග",
        "A Vinayagarathnam":"විනයගරත්නම්",
        "A.H.De Zoysa":"ඒ.එච්.ද සොයිසා",
        "Voli Nanayakkara":"වොලී නානායක්කාර",
        "Sunil Edirisinghe":" සුනිල් එදිරිසිංහ",
        "Nuwan Liyange":"නුවන් ලියනගේ",
        "D.R.Pieris":"ඩී.ආර්.පීරිස්",
        "Rohana Dharmakeerthi":"රෝහණ ධර්මකීර්ති",
        "Priyantha Dharmawansa":"ප්‍රියන්ත ධර්මවන්ශ",
        "Swarna Sri Bandara":"ස්වර්ණ ශ්‍රී බණ්ඩාර",
        "Danister Perea":"ඩැනිස්ටර් පෙරේරා",
        "Donald Ivon":"ඩොනල්ඩ් අයිවන්",
        "Amila Thenuwara":"අමිලා තේනුවර",
        "Dhammika Bandara":"ධම්මිකා බන්ඩාර",
        "Yasanath Dhammika Bandara":"යසනාත් ධම්මිකා බන්ඩාර",
        "Sunil Wimalaweera":"සුනිල් විමලවීර"

    }
    allowed_domains= [
        'sinhalasongbook.com'
        ]

    
    def start_requests(self):
        urls = [
        ]
        for i in range(1,23):
            
            urls.append('https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page='+str(i))
            
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    

    def parse(self, response):

        for quote in response.xpath('/html/body/div[1]/div[1]/div/main/article/div/div[3]/div[1]/div/div/div/h4/a/@href').getall():
            
            yield scrapy.Request(quote, callback=self.details_extractor)
            
            
    def details_extractor(self, response):
        
        self.song_name= response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/h2/span/text()').get().strip().split("–")[-1].replace("|",'')
        self.artist_name=" , ".join(["" if artist == 'Unknown' else(self.word_dic[artist.strip()] if artist.strip() in self.word_dic else self.artist_name_translator.translate(artist,src='en', dest='si').text) for artist in response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[2]/div/div/ul/li[1]/span/a/text()').getall()]).strip()
        self.genere_name=" , ".join(["" if genere == 'Unknown' else (self.word_dic[genere.strip()] if genere.strip() in self.word_dic else self.genere_name_translator.translate(genere,src='en', dest='si').text) for genere in response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[2]/div/div/ul/li[2]/span/a/text()').getall()]).strip()
        self.lyrics_by_name=" , ".join(["" if lyrics_by == 'Unknown' else (self.word_dic[lyrics_by.strip()] if lyrics_by.strip() in self.word_dic else self.lyrics_by_name_translator.translate(lyrics_by,src='en', dest='si').text) for lyrics_by in response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[1]/span/a/text()').getall()]).strip()
        self.music_by_name=" , ".join(["" if music_by == 'Unknown' else (self.word_dic[music_by.strip()] if music_by.strip() in self.word_dic else self.music_by_name_translator.translate(music_by,src='en', dest='si').text) for music_by in response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[2]/span/a/text()').getall()]).strip()
        self.lyrics=  re.sub("[a-zA-Z0-9#\[\]|\/()\t{}∆— '=_+?*°’]",""," ".join( response.xpath('//pre/text()').getall()).replace("-", " ")).strip().replace("  ", "")
        self.key = response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/h3/text()').get().split('|')[0].split(':')[-1].strip()
        if (self.song_name=="" or self.artist_name=="" or self.genere_name=="" or self.lyrics_by_name=="" or self.music_by_name=="" or self.lyrics=="" or self.key==""):
            return
        
        details= {
            'name' : self.song_name ,
            'artist' : self.artist_name ,
            'genere' : self.genere_name ,         
            'lyrics by' :self.lyrics_by_name,
            'music by' : self.music_by_name,
            # 'movie' :" , ".join([self.movie_tranlator.translate(movie,src='en', dest='si').text for movie in response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div[1]/div[3]/div/ul/li[3]/span/a/text()').getall()]).strip(),
            'key' :self.key,
            'views' : int(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div/text()').getall()[-1].split('-')[-1].split("Visits")[0].strip().replace(",", "")),
            'shares' : int(response.xpath('/html/body/div[1]/div[1]/div/main/article/div[3]/div/div[4]/span/text()').get().strip().replace(",", "")),
            'lyrics' : self.lyrics
              
            }
        self.objects.append(details)
        # with open("lyrics_objects.json", 'w', encoding="utf8") as outfile:
        #     json.dump( self.objects, outfile,indent = 4,ensure_ascii=False)
        
    def closed(self, reason):
        
        with open("lyrics_objects.json", 'w', encoding="utf8") as outfile:
           json.dump(self.objects, outfile,indent = 4,ensure_ascii=False)
           

        
        
