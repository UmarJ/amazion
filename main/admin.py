from django.contrib import admin
from main.models import Product, Account, TransactionHistory, Seller, Customer, ProductImage, Cart, Deal, Category, Review, ReviewImages, Address, Question, Answer, AnswerRating

admin.site.register(Product)
admin.site.register(Account)
admin.site.register(TransactionHistory)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Deal)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ReviewImages)
admin.site.register(Address)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerRating)
admin.site.register(ProductImage)