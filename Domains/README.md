# AuthPolicy (권한정책)

## 기능
1. Post(일기) CRUD에 대한 권한
2. Post 공유 설정에 다한 권한
3. Auth 권한 설정에 대한 권한
4. User(사용자) 삭제 및 삭제한 User의 Post 삭제(비공개) 권한
5. User 조회하는 권한

## 정보 
- list[Auth] : 가지고 있는 모든 권한을 가지고 있다.

### 추가 타입
1. Common.Policy : 권한에 대한 열거형을 가지고 있다.
   - PostCreateAndUpdatePolicy
   - PostReadPolicy
   - PostDeletePolicy
   - PostPublicAblePolicy
   - PostPlivateAblePolicy
   - 
2.  

## 기능
- check_auth()->bool : 

## 메모
- crud는 cu, r, d 따로따로 권한 부여
- 대상에 따른 권한 부여가 필요하다.

# User (계정)

## 기능

## 정보
- user_id : 사용자 계정
- name : 사용자 이름
- password : 패스워드
- uid : 식별 ID
- auth : 가지고 있는 권한
- nickname : 별명 (공유 할때 보이는 이름)
- is_delete :삭제 플레그(숨김 )

## 메모
- 이메일? : 이메일 인증...

# Post (일기)

## 기능

## 정보
- title : 일기 제목
- content : 일기 내용
- create_time : 생성 날짜(조정 가능하게 변경 필요)
- updatetime : 수정 날짜(자동 조절)
- post_id : 식별ID
- user -> maker : 생성 User
- viwer + is_share : 볼 수 있는 User / User 화이트 리스트(교환일기)
- image_list : 썸네일 (100 미만)
- is_share : 공유 여부 플레그
- is_delete :삭제 플레그(숨김)

# UserSession

## 기능
- User에 정보를 서버에서 관리합니다.
- 이를 위하여

## 정보
- key : User 정보와 매핑된 발급 키값
- user : 계정 정보
- due_to : 세션 유효기간
- is_delete : 폐기 여부 플래그

## 서비스
1. 토큰 발급 요청 서비스 : simpleuser -> key
2. 토큰 확인 요청 서비스 : key가 유효한지 확인, key, 삭자 안됐는지, 유효기간은 안지났는지 -> simpleuser