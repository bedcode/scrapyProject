import scrapy
from scrapy.loader import ItemLoader
from bookingScraper.items import BookingReviewItem

#crawl up to 6 pages of review per hotel
max_pages_per_hotel = 6

class BookingSpider(scrapy.Spider):
    name = "booking"
    start_urls = [
        #"http://www.booking.com/searchresults.html?aid=357026&label=gog235jc-city-XX-us-newNyork-unspec-uy-com-L%3Axu-O%3AosSx-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&sid=b9f9f1f142a364f6c36f275cfe47ee55&dcid=4&city=20088325&class_interval=1&dtdisc=0&from_popular_filter=1&hlrd=0&hyb_red=0&inac=0&label_click=undef&nflt=di%3D929%3Bdistrict%3D929%3B&nha_red=0&postcard=0&redirected_from_city=0&redirected_from_landmark=0&redirected_from_region=0&review_score_group=empty&room1=A%2CA&sb_price_type=total&score_min=0&ss_all=0&ssb=empty&sshis=0&rows=15&tfl_cwh=1"
        #add your city url here
        'https://www.booking.com/searchresults.it.html?aid=357026&label=gog235jc-city-XX-us-newNyork-unspec-uy-com-L%3Axu-O%3AosSx-B%3Achrome-N%3Ayes-S%3Abo-U%3Ac&sid=c14539df3e3172067926106761e03faf&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.it.html%3Faid%3D357026%3Blabel%3Dgog235jc-city-XX-us-newNyork-unspec-uy-com-L%253Axu-O%253AosSx-B%253Achrome-N%253Ayes-S%253Abo-U%253Ac%3Bsid%3Dc14539df3e3172067926106761e03faf%3Bclass_interval%3D1%3Bdest_id%3D-124105%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bmih%3D0%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_pageview_id%3Db3c96f92f0820081%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bss%3Dpavia%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne_untouched%3DNew%2520York%26%3B&ss=Pavia&ssne=Pavia&ssne_untouched=Pavia&city=-124105&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&highlighted_hotels='
    ]

    pageNumber = 1

    #for every hotel
    def parse(self, response):
        for hotelurl in response.xpath('//a[@class="hotel_name_link url"]/@href'):
            url = response.urljoin(hotelurl.extract())
            yield scrapy.Request(url, callback=self.parse_hotel, headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})

        next_page = response.xpath('//a[starts-with(@class,"paging-next")]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse, headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})

    #get its reviews page
    def parse_hotel(self, response):
        reviewsurl = response.xpath('//a[@class="show_all_reviews_btn"]/@href')
        url = response.urljoin(reviewsurl[0].extract())
        self.pageNumber = 1
        return scrapy.Request(url, callback=self.parse_reviews, headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})

    #and parse the reviews
    def parse_reviews(self, response):
        if self.pageNumber > max_pages_per_hotel:
            return
        for rev in response.xpath('//li[starts-with(@class,"review_item")]'):
            item = BookingReviewItem()
            #sometimes the title is empty because of some reason, not sure when it happens but this works
            title = rev.xpath('.//a[@class="review_item_header_content"]/span[@itemprop="name"]/text()')
            if title:
                item['title'] = title[0].extract()
                positive_content = rev.xpath('.//p[@class="review_pos"]//span/text()')
                if positive_content:
                    item['positive_content'] = positive_content[0].extract()
                negative_content = rev.xpath('.//p[@class="review_neg"]//span/text()')
                if negative_content:
                    item['negative_content'] = negative_content[0].extract()
                item['score'] = rev.xpath('.//span[@itemprop="reviewRating"]/meta[@itemprop="ratingValue"]/@content')[0].extract()
                #tags are separated by ;
                item['tags'] = ";".join(rev.xpath('.//li[@class="review_info_tag"]/text()').extract())
                yield item

        next_page = response.xpath('//a[@id="review_next_page_link"]/@href')
        if next_page:
            self.pageNumber += 1
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_reviews, headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})
