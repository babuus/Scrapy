# -*- coding: utf-8 -*-
import scrapy, requests, os, shutil
from datetime import datetime

class uk_currys:


    def __init__(self, **kwargs):
        self.to_collection = kwargs.get('to_collection')
        self.file_name = kwargs.get('file_name')
        #self.folder = kwargs.get('file_name')

 
    def parse(self, response):

        product_url = response.url
        product_code = response.xpath('//*[@id="content"]/div/section/div/p[@class="prd-code"]/text()').get()
        if product_code is not None: 
            product_code = product_code.replace('Product code: ','')
        product_name = response.xpath('//meta[@property="og:title"]/@content').get()
        #brand = response.xpath('//*[@id="content"]/div[2]/section/div[2]/h1/span[1]/text()').get()
        brand = response.xpath('//h1[@class="page-title nosp"]/span[1]/text()').get()
        mpn = response.xpath('//script/@data-flix-mpn').get()
        breadcrumb = []

        for cats in response.xpath('//*[@id="content"]/div/a/span/text()'):
            breadcrumb.append(cats.get())

        for cat in breadcrumb:
            category = cat

        all_images_url = []
        image_names = []
        main_image = []
        k=0
        for img in response.xpath('//*[@id="carousel"]/ul/li/a/@href'):
            all_images_url.append(img.get())
            k +=1
        if all_images_url!=[]:
            main_image=all_images_url[0]
        else:
            main_image=[]

        img_download = { 'main_image': main_image,'images_url':all_images_url,'file_name':self.file_name,'category':category,'product_code':product_code}
        image_names = parse_images(**img_download)
        features = []
        for feature in response.xpath('//*[@id="product-main"]/div/div/div/div/div/ul[@class="to-print"]/li/text()'):
            features.append(feature.get())

        product_specification = {}
        for specs in response.xpath('//*[@id="tab2"]/div/div/table/tbody/tr'):
            key = specs.xpath('.//th/text()').get()
            value = specs.xpath('.//td/text()').get()
            product_specification[key] = value

        old_price = response.xpath('//div[@id="product-actions-touch"]/div[@class="amounts to-print"]//span[@data-key="was-price"]/text()').get()
        new_price = response.xpath('//div[@id="product-actions-touch"]/div[@class="amounts to-print"]//strong[@data-key="current-price"]/text()').get()

        product_description = ' '.join(desc.get() for desc in response.xpath('//*[@id="product-info"]//text()'))

        total_reviews = response.xpath('//*[@id="product-main"]/div[1]/div[1]/div/a[1]/text()').get()
        prod_rating = response.xpath('//*[@id="product-main"]/div[1]/div[1]/div/span[contains(@class, "reevoo-score")]/@class').get()
        if prod_rating==None:
            prod_rating="None"
        else:
            prod_rating = prod_rating.replace('reevoo-score score-','')

        extraction_date = datetime.now()
        self.to_collection.insert_one({"source":self.file_name,"product_code":product_code,"mpn":mpn,'breadcrumb':breadcrumb,"category":category,"brand":brand,"product_name":product_name,"product_description":product_description,"product_url":product_url,"product_specification":product_specification,'main_image': main_image,"all_images_url":all_images_url,"image_names":image_names,"features":features,"new_price":new_price,"old_price":old_price,"total_reviews":total_reviews,"prod_rating":prod_rating,"extraction_date":extraction_date})

def parse_images(**kwargs):
    urls = kwargs['images_url']
    folder_location = kwargs['file_name']
    category = kwargs['category']
    product_code = kwargs['product_code']
    k=0
    image_names = []
    for url in urls:
        parent_dir = "G:\Corvid"
        Img_name = folder_location+'_'+category+'_'+product_code+'_'+str(k)+'.jpg'

        image_names.append(Img_name)
        k +=1
    return image_names
