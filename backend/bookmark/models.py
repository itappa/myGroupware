from django.db import models
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Category(models.Model):
    name = models.CharField("カテゴリ", max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "カテゴリ"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField("タグ", max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "タグ"

    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=512)
    url = models.URLField(verbose_name="URL", max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name="タグ", related_name="tags", blank=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    # ファビコン関連
    favicon_url = models.URLField(max_length=255, blank=True, null=True)

    # OGP関連
    og_title = models.CharField(max_length=200, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.URLField(max_length=255, blank=True, null=True)
    og_type = models.CharField(max_length=50, blank=True, null=True)
    og_site_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "アイテム"

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.fetch_metadata()
        super().save(*args, **kwargs)
    
    def fetch_metadata(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # ファビコンの取得
            favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
            if favicon:
                self.favicon_url = urljoin(self.url, favicon['href'])

            # OGP情報の取得
            og_title = soup.find('meta', property='og:title')
            if og_title:
                self.og_title = og_title['content']

            og_description = soup.find('meta', property='og:description')
            if og_description:
                self.og_description = og_description['content']

            og_image = soup.find('meta', property='og:image')
            if og_image:
                self.og_image = urljoin(self.url, og_image['content'])

            og_type = soup.find('meta', property='og:type')
            if og_type:
                self.og_type = og_type['content']

            og_site_name = soup.find('meta', property='og:site_name')
            if og_site_name:
                self.og_site_name = og_site_name['content']

        except Exception as e:
            print(f"Error fetching metadata: {e}")

    def __str__(self):
        return self.title