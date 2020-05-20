import json
import scrapy
 
class InfiniteScrollingSpider(scrapy.Spider):
    name = 'infinite-scrolling-python'
    scrolling_url = 'https://www.filmcompanion.in/wp-json/csco/v1/more-posts'
 
    def start_requests(self):
        yield scrapy.FormRequest(
            self.scrolling_url,
            formdata={
                #'action': 'infinite_scroll',
                'action': "csco_ajax_load_more",
                'page': '1',
                "query_vars":"{\"category_name\":\"bollywood-review\",\"error\":\"\",\"m\":\"\",\"p\":0,\"post_parent\":\"\",\"subpost\":\"\",\"subpost_id\":\"\",\"attachment\":\"\",\"attachment_id\":0,\"name\":\"\",\"pagename\":\"\",\"page_id\":0,\"second\":\"\",\"minute\":\"\",\"hour\":\"\",\"day\":0,\"monthnum\":0,\"year\":0,\"w\":0,\"tag\":\"\",\"cat\":7286,\"tag_id\":\"\",\"author\":\"\",\"author_name\":\"\",\"feed\":\"\",\"tb\":\"\",\"paged\":0,\"meta_key\":\"\",\"meta_value\":\"\",\"preview\":\"\",\"s\":\"\",\"sentence\":\"\",\"title\":\"\",\"fields\":\"\",\"menu_order\":\"\",\"embed\":\"\",\"category__in\":[],\"category__not_in\":[],\"category__and\":[],\"post__in\":[],\"post__not_in\":[36896,40871,34019,37264,44457,44397],\"post_name__in\":[],\"tag__in\":[],\"tag__not_in\":[],\"tag__and\":[],\"tag_slug__in\":[],\"tag_slug__and\":[],\"post_parent__in\":[],\"post_parent__not_in\":[],\"author__in\":[],\"author__not_in\":[],\"ignore_sticky_posts\":false,\"suppress_filters\":false,\"cache_results\":true,\"update_post_term_cache\":true,\"lazy_load_term_meta\":true,\"update_post_meta_cache\":true,\"post_type\":\"\",\"posts_per_page\":12,\"nopaging\":false,\"comments_per_page\":\"50\",\"no_found_rows\":false,\"order\":\"DESC\"}",
                "query_args":"{\"archive_type\":\"masonry\",\"show_first\":false,\"columns\":2,\"meta_cat\":false,\"meta\":true,\"summary\":true,\"standard_summary\":\"excerpt\",\"more_button\":false,\"reduce_margin\":false,\"orientation\":\"landscape\",\"list_width\":\"6\",\"widgets\":false,\"widgets_sidebar\":\"sidebar-archive\",\"widgets_after\":3,\"widgets_repeat\":false,\"highlight\":\"featured\",\"pagination_type\":\"ajax\",\"infinite_load\":true}"
            },
            callback=self.parse_page,
            meta={'page': 1},
        )
 
    def parse_page(self, response):
        next_page = response.meta.get('page') + 1
        print('next_page:', next_page)
        #print(response.text)
 
        json_data = json.loads(response.text)
        #print(json_data.keys())        
        #print('success:', json_data.get('success'))        
        #print('data:', json_data.get('data'))        
       
        #if json_data.get('type') != 'success':  # WRONG
        if not json_data.get('success') or not json_data.get('data') or not json_data['data'].get('content'):
            return
       
        #articles = scrapy.Selector(text=json_data.get('html')).css('article')  # WRONG
        articles = scrapy.Selector(text=json_data['data']['content']).css('article')
        for article in articles:
            yield {
                'page_title': article.css('h2.entry-title a ::text').extract_first().strip(),
                'review_link': article.css('h2.entry-title a ::attr(href)').extract_first().strip(),
            }
        print('next page >>>')
        yield scrapy.FormRequest(
            self.scrolling_url,
            formdata={
                'action': "csco_ajax_load_more",
                'page': str(next_page),
                "query_vars":"{\"category_name\":\"bollywood-review\",\"error\":\"\",\"m\":\"\",\"p\":0,\"post_parent\":\"\",\"subpost\":\"\",\"subpost_id\":\"\",\"attachment\":\"\",\"attachment_id\":0,\"name\":\"\",\"pagename\":\"\",\"page_id\":0,\"second\":\"\",\"minute\":\"\",\"hour\":\"\",\"day\":0,\"monthnum\":0,\"year\":0,\"w\":0,\"tag\":\"\",\"cat\":7286,\"tag_id\":\"\",\"author\":\"\",\"author_name\":\"\",\"feed\":\"\",\"tb\":\"\",\"paged\":0,\"meta_key\":\"\",\"meta_value\":\"\",\"preview\":\"\",\"s\":\"\",\"sentence\":\"\",\"title\":\"\",\"fields\":\"\",\"menu_order\":\"\",\"embed\":\"\",\"category__in\":[],\"category__not_in\":[],\"category__and\":[],\"post__in\":[],\"post__not_in\":[36896,40871,34019,37264,44457,44397],\"post_name__in\":[],\"tag__in\":[],\"tag__not_in\":[],\"tag__and\":[],\"tag_slug__in\":[],\"tag_slug__and\":[],\"post_parent__in\":[],\"post_parent__not_in\":[],\"author__in\":[],\"author__not_in\":[],\"ignore_sticky_posts\":false,\"suppress_filters\":false,\"cache_results\":true,\"update_post_term_cache\":true,\"lazy_load_term_meta\":true,\"update_post_meta_cache\":true,\"post_type\":\"\",\"posts_per_page\":12,\"nopaging\":false,\"comments_per_page\":\"50\",\"no_found_rows\":false,\"order\":\"DESC\"}",
                "query_args":"{\"archive_type\":\"masonry\",\"show_first\":false,\"columns\":2,\"meta_cat\":false,\"meta\":true,\"summary\":true,\"standard_summary\":\"excerpt\",\"more_button\":false,\"reduce_margin\":false,\"orientation\":\"landscape\",\"list_width\":\"6\",\"widgets\":false,\"widgets_sidebar\":\"sidebar-archive\",\"widgets_after\":3,\"widgets_repeat\":false,\"highlight\":\"featured\",\"pagination_type\":\"ajax\",\"infinite_load\":true}"
            },
            callback=self.parse_page,
            meta={'page': next_page},
        )