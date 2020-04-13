class Book(object):

    def __init__(self, book_id='', name='', author='', press='', category_ids='',
                 words_count='', cover='', intro='', catalog='', attach_url='', create_time='',
                 update_time='', status=''):
        super(Book, self).__init__()
        self.book_id = book_id
        self.name = name
        self.author = author
        self.press = press
        self.category_ids = category_ids
        self.words_count = words_count
        self.cover = cover
        self.intro = intro
        self.catalog = catalog
        self.attach_url = attach_url
        self.create_time = create_time
        self.update_time = update_time
        self.status = status

    def __str__(self):
        return '''(book_id:{0},name:{1},author:{2},press:{3},category_ids:{4},words_count:{5},cover:{6},intro:{7},
        catalog:{8},attach_url:{9},create_time:{10},update_time:{11},status:{12})''' \
            .format(self.book_id, self.name, self.author, self.press, self.category_ids, self.words_count, self.cover,
                    self.intro, self.catalog, self.attach_url, self.create_time, self.update_time, self.status)

    __repr__ = __str__
