import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
filename = 'export'
import logging
from scrapy.utils.log import configure_logging

class RowSpider(scrapy.Spider):

    name = "wsba"
    custom_settings = {
    'FEEDS': {
      f'{filename}.csv': {
        'format': 'csv',
        'overwrite': True
      }
    }
    }
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    def start_requests(self):
        urls = [
            'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&LicenseType=LLLT&County=Thurston&Country=USA',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_firstpage, dont_filter = True)

    def parse_firstpage(self, response):
        all_pages = []
        results_count = response.css('.results-count::text').get()
        page_count = results_count.rsplit(" ")
        p_count = int(page_count[0]) / 20
        print(round(p_count))
        if (round(p_count)>0) :
            all_pages.append(response.url)
            for x in range(1, round(p_count)):
                all_pages.append(response.url+'&Page='+str(x))
            for all_page in all_pages:
                yield scrapy.Request(all_page, callback=self.parse, dont_filter = True)
        else:
            page_urls = []
            r = response.css('.grid-row').getall()
            for row in r:
                instr = str(row)
                parts = instr.rsplit("'")
                page_urls.append('https://www.mywsba.org/PersonifyEbusiness/' + parts[1])
            print(page_urls)

            for page_url in page_urls:
                yield scrapy.Request(page_url, callback=self.parse_page, dont_filter = True)


    def parse(self, response):

        page_urls = []
        r = response.css('.grid-row').getall()
        for row in r:
            instr = str(row)
            parts = instr.rsplit("'")
            page_urls.append('https://www.mywsba.org/PersonifyEbusiness/' + parts[1])
        print(page_urls)

        for page_url in page_urls:
            yield scrapy.Request(page_url, callback=self.parse_page, dont_filter = True)



    def parse_page(self, response):
        item = Row()
        item['name'] = response.css('.name::text').get()
        item['l_number'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblMemberNo::text').get()
        item['l_type'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblLicenseType::text').get()
        item['l_status'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblStatus::text').get()
        item['EligibleToPractice'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblEligibleToPractice::text').get()
        item['WaAdmitDate'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblWaAdmitDate::text').get()
        item['Address'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblAddress::text').get()
        item['Email'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblEmail::text').get()
        item['Phone'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblPhone::text').get()
        item['Fax'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblFax::text').get()
        item['Website'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_hlWebsite::text').get()
        item['TDD'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblTDD::text').get()
        item['Employer'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblEmployer::text').get()
        item['FirmSize'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblFirmSize::text').get()
        item['PracticeAreas'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblPracticeAreas::text').get()
        item['Languages'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblLanguages::text').get()
        item['PLILLLTLPO'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_divPLILLLTLPO::text').get().strip()
        item['HasJudicialService'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblHasJudicialService::text').get()
        item['Committees'] = response.css('#dnn_ctr2977_DNNWebControlContainer_ctl00_lblCommittees::text').get()
        return item


class Row(scrapy.Item):
    name = scrapy.Field()
    l_number = scrapy.Field()
    l_type = scrapy.Field()
    l_status = scrapy.Field()
    EligibleToPractice = scrapy.Field()
    WaAdmitDate = scrapy.Field()
    Address = scrapy.Field()
    Email = scrapy.Field()
    Phone = scrapy.Field()
    Fax = scrapy.Field()
    Website = scrapy.Field()
    TDD = scrapy.Field()
    Employer = scrapy.Field()
    FirmSize = scrapy.Field()
    PracticeAreas = scrapy.Field()
    Languages = scrapy.Field()
    PLILLLTLPO = scrapy.Field()
    HasJudicialService = scrapy.Field()
    Committees = scrapy.Field()

