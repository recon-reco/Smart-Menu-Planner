from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

"""
이 코드 스니펫은 Django 프레임워크에서 관리자(admin) 인터페이스를 설정하는 방법을 보여줍니다. 각 코드의 의미와 사용된 모듈, 함수에 대해 자세히 설명하겠습니다.

1. from django.contrib import admin
모듈: django.contrib.admin
설명: Django의 admin 모듈을 가져옵니다. 이 모듈은 Django 프로젝트에서 제공되는 관리 인터페이스를 구성하는 데 사용됩니다. Django 관리자 인터페이스는 데이터베이스 모델을 웹 인터페이스를 통해 관리할 수 있도록 해줍니다.
2. from .models import Post, Category
모듈: models.py (현재 앱의 모델)
설명: 현재 Django 앱의 models.py 파일에 정의된 Post와 Category 모델을 가져옵니다. 이 모델들은 데이터베이스 테이블과 연결된 Django의 ORM(Object-Relational Mapping) 객체입니다.
3. admin.site.register(Post)
함수: admin.site.register
설명: Post 모델을 관리자 사이트에 등록합니다. 이렇게 등록된 모델은 Django 관리자 인터페이스에서 관리할 수 있게 됩니다. 기본적으로 등록만 할 경우, Django는 자동으로 기본 폼과 리스트를 생성하여 제공하지만, 별도의 커스터마이징이 필요할 경우 추가적으로 설정할 수 있습니다.
4. class CategoryAdmin(admin.ModelAdmin):
클래스: admin.ModelAdmin
설명: Category 모델의 관리자 인터페이스를 커스터마이징하기 위해 CategoryAdmin 클래스를 정의합니다. admin.ModelAdmin은 Django에서 제공하는 클래스이며, 이를 상속하여 다양한 관리자 화면의 동작과 외형을 커스터마이징할 수 있습니다.
5. prepopulated_fields = {'slug': ('name',)}
속성: prepopulated_fields

설명: 이 속성은 관리자 인터페이스에서 특정 필드를 미리 채워지도록 설정하는 데 사용됩니다. 위 코드에서는 slug 필드를 name 필드의 값을 기반으로 자동으로 채우도록 설정합니다. 예를 들어, name 필드에 "My Category"라고 입력하면, slug 필드에는 자동으로 "my-category"가 입력됩니다.

'slug': 데이터베이스 모델의 필드 이름. 일반적으로 URL에 사용하기 위해 필드 값이 자동으로 형식화됩니다.
('name',): 미리 채워질 필드의 값이 참조하는 필드(들)의 이름. 튜플로 여러 필드를 지정할 수 있지만, 여기서는 단일 필드인 name만 지정되었습니다.
6. admin.site.register(Category, CategoryAdmin)
함수: admin.site.register
설명: Category 모델을 관리자 사이트에 등록하면서, CategoryAdmin 클래스를 사용해 해당 모델의 관리자 인터페이스를 커스터마이징합니다. 이로 인해 Category 모델을 관리할 때, 앞서 정의한 prepopulated_fields 등의 설정이 적용된 형태로 관리자 인터페이스가 제공됩니다.
전체 코드의 흐름
Post와 Category라는 두 가지 모델이 있는데, 이 모델들을 Django의 관리자 인터페이스에 등록하고 관리할 수 있도록 설정합니다.
Post 모델은 기본 설정으로 관리자 인터페이스에 등록되고, Category 모델은 CategoryAdmin 클래스를 통해 커스터마이징된 설정으로 등록됩니다.
Category 모델의 slug 필드는 name 필드에 입력된 값에 따라 자동으로 채워지도록 설정됩니다.
이 코드는 Django 관리자 인터페이스를 통해 모델 데이터를 보다 효율적으로 관리할 수 있도록 도와줍니다. Django의 admin 모듈은 기본적으로 제공되는 강력한 기능을 통해 개발자가 최소한의 코드로도 효과적인 데이터 관리를 할 수 있게 해줍니다."""