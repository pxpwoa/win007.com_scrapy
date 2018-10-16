# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
import random
from scrapy.conf import settings
from scrapy import log
import base64
import pickle
import requests
from scrapy.http import HtmlResponse
import http.client


class ProxyMiddleware(object):
    def __init__(self):
        with open('proxy_pool.pickle', 'rb') as f:
            self.PROXIES = pickle.load(f)


    def process_request(self, request, spider):

        proxy = random.choice(self.PROXIES)
        print ("**************ProxyMiddleware no pass************" + proxy)
        request.meta['proxy'] = proxy
        request.meta['dont_redirect']= True
        request.meta['handle_httpstatus_list']= [302, 400, 403,404, 408,500,502, 503, 504]



class NowgoalSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
