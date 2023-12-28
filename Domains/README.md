# AuthPolicy (권한정책)

## 기능
1. Post(일기) CRUD에 대한 권한
2. Post 공유 설정에 다한 권한
3. Auth 권한 설정에 대한 권한
4. User 조회하는 권한
5. ~~User 로그인 정지 해제 권한~~
6. User(사용자) 삭제 및 삭제한 User의 Post 삭제(비공개) 권한

## 정보
1. Common.AuthArchives : 계정이 가지고 있는 모든 권한을 표현한다.
   - List[Auth]
2. Common.UnionAuth : 서비스를 사용하기 위한 권한 정의를 표현한다. 합집합 형태로 하나만 속해도 된다.
   - List[ Union[Auth,UnionAuth,IntersectionAuth] ]
3. Common.IntersectionAuth : 서비스를 사용하기 위한 권한 정의를 표현한다. 교집합 형태로 모든 권한을 가져야 된다.
   - List[ Union[Auth,UnionAuth,IntersectionAuth] ]
### 추가 타입
1. Common.Policy : 권한에 대한 열거형을 가지고 있다. ( 대상 + 행위 + 가능정책 ) 으로 이름 기술 
   - None : 권한 없음 
   - PostCreateAndUpdateAblePolicy : 일기 생성 수정 권한
   - PostReadAblePolicy :  일기 읽기 권한
   - PostDeleteAblePolicy : 일기 삭제(비공개 플레그) 할 수 있는 권한 권한
   - PostPublicAblePolicy  : 일기 공개 할수 있는 권한
   - PostPrivateAblePolicy : 일기 비공개 할수 있는 권한
   - UserAuthLockOfPostCreateAndUpdatePolicy : 사용자의 일기 생성 수정 권한 정지시킬 수 있는 권한
   - UserAuthUnlockOfPostCreateAndUpdatePolicy : 사용자의 일기 생성 수정 권한 재개시킬 수 있는 권한
   - ~~UserLoginUnlockAblePolicy : 사용자의 로그인 정지 해제 시킬 수 있는 권한~~
   - UserDataReadAblePolicy : 사용자 데이터를 확인하는 권한
   - UserDataDeleteAblePolicy : 사용자 데이터를 삭제(비공개 플레그) 할수 있는 권한 
2. Common.TargetRange : 권한을 행사할 수 있는 범위대한 열거형을 가지고 있다.
   - Own : 자신이 소유한 것에 대해 행사
   - Borrow : 빌려도 된다고 허용된 것에 대해 행사
   - Allowed : 모두에게 허용된 것에 대하여 행사
   - All : 모든 것에 대하여 행사
3. Common.Auth : Common.Policy와 Common.TargetRange가 결합하여 권한을 표현
   - policy : 행사 가능한 권한 정책을 담고 있다.
   - target_range : 권한을 행사할 수 있는 범위를 담고 있다.
  
## 기한
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
- last_update_date : 마지막으로 일기 쓴 날짜
- count_of_post : 마지막 날에 일기 쓴 횟수(횟수 제한을 두기 위함)
- count_of_login_fail : 로그인 시도 연속 실패횟수 기록
- login_lock_data : 로그인 금지에 관련된 데이터. 정지 여부, 정지 시간 등등 
- delete_flag :삭제 플레그(숨김)

## 메모
- 이메일? : 이메일 인증...

# Post (일기)

## 기능

## 제한사항
- 하루에 10개까지 생성가능
- 이미지 한장만 가능
- 사용할 수 없는 공유일기는 없다.
- 공유일기의 정렬 순서는 공유순서이다.

## 정보
- title : 일기 제목
- content : 일기 내용 (2000자 제한)
- create_time : 생성 날짜
- updatetime : 수정 날짜(자동 조절)
- post_id : 식별ID
- user -> maker : 생성 User
- target_time : 일기의 날짜 시간은 제거 된다.(조정 가능하게 변경 필요)
- ~~viwer + is_share : 볼 수 있는 User / User 화이트 리스트(교환일기)~~
- image_list : 썸네일 (100 미만)
- is_share : 공유 여부 플레그
- delete_flag :삭제 플레그(숨김)

# UserSession

## 기능
- User에 정보를 서버에서 관리합니다.
- 이를 위하여

## 정보
- key : User 정보와 매핑된 발급 키값
- user : 계정 정보
- due_to : 세션 유효기간
- delete_flag : 폐기 여부 플래그

## 서비스
1. 토큰 발급 요청 서비스 : simpleuser -> key
2. 토큰 확인 요청 서비스 : key가 유효한지 확인, key, 삭자 안됐는지, 유효기간은 안지났는지 -> simpleuser

