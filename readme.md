# 28-1st-MRMRZR-backend

> 본 repository는 웹 개발 학습을 위해 ZARA(https://www.zara.com/kr/) 사이트를 클론코딩하였습니다.
> 짧은 기간동안 기능 구현에 보다 집중하기 위해 User, Product, Cart 앱까지 기능 구현하였습니다.


## 개발 인원 및 기간

+ 개발기간: 2021.12.27. ~ 2022.01.07.
	+ Frontend: 김선주, 안현재, 정해수 (repository: https://github.com/wecode-bootcamp-korea/28-1st-MRMRZR-frontend)
	
	+ Backend
		+ Backend 공통: ERD, CSV Uploader
		+ :wink: 이정석 - Product - 제품 전체 페이지
		+ :blush: 지원석 - Product - 제품 상세 페이지, Decorator, AWS 배포
		+ :grinning: 장우경 - 초기 셋팅, User, Cart


## Demo

> 회원가입 및 로그인 영상
[회원가입 및 로그인 영상](https://www.youtube.com/watch?v=R29AJkFlXJE&list=PLIT4ViYX2bfhXm4Ia6TIfcTpih7-Ch1PT)

> 제품 리스트 뷰, 상세페이지, 장바구니 앱 영상
[제품 리스트 뷰, 상세페이지, 장바구니 앱 영상](https://youtu.be/TwTx48PnCc0?list=PLIT4ViYX2bfhXm4Ia6TIfcTpih7-Ch1PT)


## DB modeling

![MRMRZARA](https://user-images.githubusercontent.com/75561289/148708315-68cae5ee-2b37-49c0-a29f-19a36d7b6f65.png)


## 협업 도구

+ Github
+ [Trello 바로가기](https://trello.com/b/2f3aGMvW/first-sprint)
+ Slack


## 사용 기술

+ Git
+ Django
+ Python
+ MySQL
+ AWS


## Library

+ JWT


## 구현 기능

### User
+ 회원가입: 정규표현식을 활용하여 email 및 비밀번호 유효성 체크, 이메일 중복 여부 체크, Bycrypt 활용하여 비밀번호 암호화 후 DB에 저장.

+ 로그인: Bcrypt 활용하여 비밀번호 복호화하여 체크 후 JWT 발급

### Product
+ 제품 전체 리스트 조회, 정렬, 필터 기능 구현

+ 제품 상세 페이지 조회 기능 구현

### Cart
+ Decorator 적용하여 token 통해서 유저 인증 후 장바구니 앱 사용할 수 있도록 기능 구현

+ 장바구니에 제품 추가, 수량 수정 기능 구현 (POST)

+ 장바구니 제품 리스트 조회 기능 구현 (GET)

+ 장바구니 제품 삭제 기능 구현 (DELETE)


## Reference

+ 이 프로젝트는 ZARA 사이트를 참조하여 학습 목적으로 만들었습니다.
+ 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제가 될 수 있습니다.
+ 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

