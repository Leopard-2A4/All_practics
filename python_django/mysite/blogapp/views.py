from django.db.models import Prefetch
from django.views.generic import ListView
from .models import Article, Tag

class ArticlesListView(ListView):
    template_name = "blogapp/article-list.html"
    context_object_name = "articles"

    queryset = (
        Article.objects
        .select_related(
            "author",
            "category",
        )
        .only(
            "title",
            "pub_date",
            "author__name",
            "category__name",
        )
        .prefetch_related(
            Prefetch(
                "tag",queryset=Tag.objects.only("name"))
        )
    ).defer("content")