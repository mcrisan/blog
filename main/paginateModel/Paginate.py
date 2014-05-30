
class PaginateObject():
    """Creates the post model
    
    Functions:
    dump_datetime -- Deserialize datetime object into string form for JSON processing.
    serialize -- Creates a dict from post object
    serialize2 -- Creates a dict from post object
    top_posts -- Returns top posts by the number of comments
    posts_category_status -- Returns posts from category, based on post status
    posts_tag_status -- Returns from tags, based on post status
    get_comments_by_post -- Returns comments from post
    check_category -- Returnd s list with categories assigned to a post
    """
    items = []
    has_prev = None
    has_next = None
    prev_num = None
    next_num = None
    
    def __init__(self, items=[], has_prev=None, has_next=None, 
                 prev_num=None, next_num=None):
        self.has_prev = has_prev
        self.has_next = has_next
        self.prev_num = prev_num
        self.next_num = next_num
        self.items = items