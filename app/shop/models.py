from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.urls import reverse


RATING_CHOICES = [
    (1, "1 - Very bad"),
    (2, "2 - Bad"),
    (3, "3 - Okay"),
    (4, "4 - Great"),
    (5, "5 - Excellent"),
]


class Shop(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        default_related_name = "shop"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        default_related_name = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductQuerySet(models.query.QuerySet):

    def available(self):
        return self.filter(available=True)

    def non_available(self):
        return self.filter(available=False)


class ProductManager(models.Manager):

    def get_query_set(self):
        return ProductQuerySet(self.model)

    def available(self):
        return self.get_query_set().available()

    def non_available(self):
        return self.get_query_set().non_available()


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, db_index=True)
    image = models.ImageField(upload_to='image_products/%Y/%m/%d', default='image_products/no_img.png')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        default_related_name = "products"

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id, self.slug])

    def get_shop_slug(self):
        shop = Shop.objects.get(name=self.shop)
        shop = shop.slug
        return reverse('product_list_by_shop',
                       args=[shop])

    def get_rating(self):
        product = Product.objects.get(id=self.id, slug=self.slug)
        rating = product.reviews.filter(show=True).aggregate(Avg('rating'))
        return rating

    def get_rating_votes(self):
        product = Product.objects.get(id=self.id, slug=self.slug)
        count = product.reviews.filter(show=True).count()
        return count

    def __str__(self):
        return self.name


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    body = models.TextField()
    show = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return "Review №{} for {}".format(self.id, self.product)


class ReviewsAnswer(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='admin')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Answer on {}".format(self.review)
