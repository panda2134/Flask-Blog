from flask.views import MethodView


class CommentsView(MethodView):
    @staticmethod
    def all_comments():
        pass

    @staticmethod
    def get_comments_in_uri(uri):
        pass

    @staticmethod
    def post_comment_in_uri(uri):
        pass

    @staticmethod
    def toggle_comments_in_uri(uri):
        pass

    @staticmethod
    def get_comment_by_id(uri, comment_id):
        pass

    @staticmethod
    def remove_comment_by_id(uri, comment_id):
        pass
