from database.db_manager import DatabaseManager

class Category:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_all_categories(self):
        query = 'SELECT * FROM categories'
        return self.db.fetch_all(query)
    
    def get_category_by_id(self, category_id):
        query = 'SELECT * FROM categories WHERE category_id = ?'
        return self.db.fetch_one(query, (category_id,))
    
    def get_categories_dict(self):
        """Returns dict of {keyword: category_id} for matching"""
        categories = self.get_all_categories()
        keywords_dict = {}
        
        for cat in categories:
            if cat['keywords']:
                keywords_list = cat['keywords'].split(',')
                for keyword in keywords_list:
                    keyword = keyword.strip().lower()
                    keywords_dict[keyword] = {
                        'category_id': cat['category_id'],
                        'category_name': cat['category_name'],
                        'category_type': cat['category_type']
                    }
        
        return keywords_dict