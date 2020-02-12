from abc import abstractmethod


class CommentMixin:
    @abstractmethod
    def comment_loc(self) -> str:
        """
        Any class using this mixin should implement this.
        :return: a string denoting the current page
        """
        pass
