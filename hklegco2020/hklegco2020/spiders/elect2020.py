import scrapy, re, time
from hklegco2020.items import Hklegco2020Item


class Elect2020Spider(scrapy.Spider):
    name = 'elect2020'
    allowed_domains = ['elections.gov.hk']
    start_urls = ['https://www.elections.gov.hk/legco2020/eng/nominat2.html']
    nominees = {}
    #items = []

    def parse(self, response):
        tables = response.xpath('//a[contains(@id, "html")]/@href').extract()
        for i in tables:
            yield scrapy.Request(response.urljoin(i), self.parse_table)
        #time.sleep(5)
        if re.search('/eng', response.url):
            yield scrapy.Request('https://www.elections.gov.hk/legco2020/chi/nominat2.html', self.parse)

    def parse_table(self, response):
        if re.search('/LC[1-5]', response.url):
            table_type_e = 'Geographical Constituencies'
            table_type_c = '地方選區'
        else:
            table_type_e = 'Functional Constituencies'
            table_type_c = '功能界別'
        table_code = re.sub('^.*/pdf/', '', response.url)
        table_code = re.sub('_[ce].*$', '', table_code)
        print(table_code)
        if re.search('_e.html$', response.url):
            self.nominees[table_code] = []
        table = response.xpath('//div[@class="main"]/table/tr')
        count = 0
        nominee_count = 0
        district = ''
        for i in table:
            row = i.xpath('td/text()').extract()
            if len(row) > 0:
                if row[1] != '\xa0':
                    if row[0] != '\xa0':
                        if row[0] == district:
                            nominee_count += 1
                        else:
                            nominee_count = 1
                        district = row[0]
                    if re.search('_e.html$', response.url):
                        nominee = {}
                        #nominee['table_type_e'] = table_type_e
                        #nominee['table_type_c'] = table_type_c
                        nominee['district_e'] = district
                        #nominee['nominee_count'] = nominee_count
                        nominee['name_e'] = row[1]
                        nominee['gender_e'] = row[3]
                        nominee['date_of_nomination'] = row[6]
                        if row[2] != '\xa0':
                            nominee['alias_e'] = row[2]
                        else:
                            nominee['alias_e'] = ''
                        if row[4] != '\xa0':
                            nominee['occupation_e'] = row[4]
                        else:
                            nominee['occupation_e'] = ''
                        if row[5] != '\xa0':
                            nominee['affiliation_e'] = row[5]
                        else:
                            nominee['affiliation_e'] = ''
                        self.nominees[table_code] += [ nominee ]
                        #print(len(self.nominees))
                        #print(nominee)
                    else:
                        item = Hklegco2020Item()
                        item['table_type_e'] = table_type_e
                        item['table_type_c'] = table_type_c
                        item['table_code'] = table_code
                        item['district_c'] = district
                        item['district_e'] = self.nominees[table_code][count]['district_e']
                        item['nominee_count'] = nominee_count
                        item['name_c'] = row[1]
                        item['name_e'] = self.nominees[table_code][count]['name_e']
                        item['alias_e'] = self.nominees[table_code][count]['alias_e']
                        item['gender_c'] = row[3]
                        item['gender_e'] = self.nominees[table_code][count]['gender_e']
                        item['occupation_e'] = self.nominees[table_code][count]['occupation_e']
                        item['affiliation_e'] = self.nominees[table_code][count]['affiliation_e']
                        item['date_of_nomination'] = self.nominees[table_code][count]['date_of_nomination']
                        if row[2] != '\xa0':
                            item['alias_c'] = row[2]
                        else:
                            item['alias_c'] = ''
                        if row[4] != '\xa0':
                            item['occupation_c'] = row[4]
                        else:
                            item['occupation_c'] = ''
                        if row[5] != '\xa0':
                            item['affiliation_c'] = row[5]
                        else:
                            item['affiliation_c'] = ''
                        yield item
                        #print(item)
                        #self.items.append(item)
                    count += 1




