from django.contrib import admin

# Register your models here.
from newsfeed.models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post_img', 'user', 'created_at')
    search_fields = ('content', 'user__username')
    list_filter = ('created_at', 'user')
    readonly_fields = ('created_at', 'updated_at')
  
    ordering = ('-created_at',)

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'post__content')
    list_filter = ('created_at', 'user', 'post')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('is_reply', 'is_deleted', 'is_edited')
        return self.readonly_fields

admin.site.register(Comment, CommentAdmin)