from django.urls import path
from main.views import (
    show_main, add_product, show_product, show_xml, show_json,
    show_xml_by_id, show_json_by_id, register, login_user, logout_user,
    edit_product, delete_product,
    # AJAX endpoints
    get_products_json, create_product_ajax, update_product_ajax,
    delete_product_ajax, login_ajax, register_ajax,
    # News views
    show_news, create_news, show_news_detail, show_news_xml, show_news_json,
    show_news_xml_by_id, show_news_json_by_id, edit_news, delete_news,
    add_news_entry_ajax, create_news_flutter
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),

    # AJAX endpoints
    path('api/products/', get_products_json, name='get_products_json'),
    path('api/products/create/', create_product_ajax, name='create_product_ajax'),
    path('api/products/<uuid:id>/update/', update_product_ajax, name='update_product_ajax'),
    path('api/products/<uuid:id>/delete/', delete_product_ajax, name='delete_product_ajax'),
    path('api/login/', login_ajax, name='login_ajax'),
    path('api/register/', register_ajax, name='register_ajax'),

    # News URLs
    path('news/', show_news, name='show_news'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>/', show_news_detail, name='show_news_detail'),
    path('news/xml/', show_news_xml, name='show_news_xml'),
    path('news/json/', show_news_json, name='show_news_json'),
    path('news/xml/<str:news_id>/', show_news_xml_by_id, name='show_news_xml_by_id'),
    path('news/json/<str:news_id>/', show_news_json_by_id, name='show_news_json_by_id'),
    path('news/<uuid:id>/edit', edit_news, name='edit_news'),
    path('news/<uuid:id>/delete', delete_news, name='delete_news'),
    path('create-news-ajax', add_news_entry_ajax, name='add_news_entry_ajax'),
    path('create-news-flutter/', create_news_flutter, name='create_news_flutter'),
]