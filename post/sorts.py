from datetime import datetime
from math import log


class Hot:
    """Hot sort ranking

    From:
        https://github.com/reddit-archive/reddit/blob/753b17407e9a9dca09558526805922de24133d53/r2/r2/lib/db/_sorts.pyx
        https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9
    """
    name = "hot"

    @staticmethod
    def epoch_seconds(date):
        epoch = datetime(1970, 1, 1)
        td = date - epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    def sort(self, likes, created_at):
        s = likes
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = self.epoch_seconds(created_at) - 1134028003
        return round(sign * order + seconds / 45000, 7)

    def order_by(self, posts):
        """Order django list by hot sort

        From:
            https://github.com/croach/tutsplus-django/blob/f4daa71e6248f7131226bc03d041f1cc798d6b04/stories/views.py
        """
        ranked_posts = sorted(
            [
                (self.sort(post.liked_by.count(), post.created_at()), post)
                for post in posts
            ],
            reverse=True,
        )
        return [post for _, post in ranked_posts]


class New:
    """New sort ranking"""
    name = "new"
