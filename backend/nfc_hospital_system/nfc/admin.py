# nfc/admin.py

from django.contrib import admin
from .models import NFCTag, TagLog, NFCTagExam


# NFCTagExam을 NFCTag Admin에 인라인으로 추가
class NFCTagExamInline(admin.TabularInline):
    """
    NFCTag 모델에 NFCTagExam을 인라인으로 추가하여 함께 관리합니다.
    """
    model = NFCTagExam
    extra = 1  # 기본으로 보여줄 빈 폼의 개수
    fields = ('exam_id', 'exam_name', 'exam_room', 'is_active')



# NFCTag 모델 관리자 설정
@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    """
    Django 관리자 페이지에서 NFCTag 모델을 관리합니다.
    """
    list_display = (
        'code', 'get_location_display', 'tag_uid', 'is_active',
        'last_scanned_at', 'created_at', 'updated_at'
    )
    list_filter = (
        'is_active', 'building', 'floor', 'created_at'
    )
    search_fields = (
        'code', 'tag_uid', 'building', 'room', 'description'
    )
    # 폼에서 필드 그룹화 및 정리
    fieldsets = (
        (None, {
            'fields': ('tag_uid', 'code', 'description')
        }),
        ('위치 정보', {
            'fields': ('building', 'floor', 'room', 'x_coord', 'y_coord')
        }),
        ('상태 및 기록', {
            'fields': ('is_active', 'last_scanned_at'),
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('tag_id', 'last_scanned_at', 'created_at', 'updated_at')
    ordering = ('building', 'floor', 'room')
    inlines = [NFCTagExamInline] # NFCTagExam을 인라인으로 포함

    # 액션 추가
    actions = ['activate_tags', 'deactivate_tags']

    def activate_tags(self, request, queryset):
        """선택된 NFC 태그를 활성화합니다."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated}개의 NFC 태그가 활성화되었습니다.')
    activate_tags.short_description = "선택된 NFC 태그 활성화"

    def deactivate_tags(self, request, queryset):
        """선택된 NFC 태그를 비활성화합니다."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated}개의 NFC 태그가 비활성화되었습니다.')
    deactivate_tags.short_description = "선택된 NFC 태그 비활성화"


# TagLog 모델 관리자 설정
@admin.register(TagLog)
class TagLogAdmin(admin.ModelAdmin):
    """
    Django 관리자 페이지에서 TagLog 모델을 관리합니다.
    로그 기록은 주로 조회용으로 사용되므로, 수정/추가/삭제를 비활성화합니다.
    """
    list_display = (
        'timestamp', 'user', 'tag', 'action_type'
    )
    list_filter = (
        'action_type', 'timestamp', 'tag__building', 'tag__floor',
        'user', 'tag'
    )
    search_fields = (
        'user__name', 'user__email', 'tag__code', 'tag__description',
        'tag__building', 'tag__room'
    )
    raw_id_fields = ('user', 'tag') # ForeignKey 필드에 대해 검색 가능한 입력 필드 제공
    date_hierarchy = 'timestamp' # 스캔 시간 기준으로 날짜별 탐색
    ordering = ('-timestamp',)

    # 로그 모델은 조회를 목적으로 하므로, 수정/추가/삭제를 비활성화합니다.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = (
        'tag', 'user', 'action_type', 'timestamp'
    )


# NFCTagExam 모델 관리자 설정 (인라인으로 사용하지 않고 단독으로 관리할 경우)
# @admin.register(NFCTagExam)
# class NFCTagExamAdmin(admin.ModelAdmin):
#     list_display = ('tag', 'exam_id', 'exam_name', 'exam_room', 'is_active')
#     list_filter = ('is_active', 'exam_name', 'exam_room', 'tag__building')
#     search_fields = ('exam_id', 'exam_name', 'exam_room', 'tag__code')
#     raw_id_fields = ('tag',)
#     ordering = ('tag__code', 'exam_name')
