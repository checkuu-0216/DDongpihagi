'''하늘에서 떨어지는 똥 피아기 게임 만들기

[게임조건]
1.캐릭터는 화면 가장 아래에 위치, 좌우로만 이동 가능
2.똥은 화면 가장 위에서 떨어짐, x 좌표는 매번 랜덤으로 설정
3.캐릭터가 똥을 피하면 다음 똥이 다시 떨어짐
4.캐릭터가 똥과 충돌하면 게임 종료
5.FPS는 30으로 고정
6.시간에 따른 똥 속도 증가, 똥 리젠 속도 증가 및 점수 추가 
7.똥 피하면 점수 추가

[게임이미지]
1. 배경 : 640 * 480(세로 가로) - background.png
2. 캐릭터 : 70 * 70 - character.png
3. 똥 : 70 * 70 - enemy.png'''

import pygame
import random

pygame.init() #초기화

#화면 크기 설정
screen_width = 480 #가로
screen_height = 640 #세로
screen = pygame.display.set_mode((screen_width , screen_height))

#화면 타이틀 설정
pygame.display.set_caption("game test")

#FPS
clock = pygame.time.Clock()

# 배경이미지 불러오기
background = pygame.image.load("C:\\Users\\pc\\Desktop\\python\\PythonGameClone1\\pygame_basic\\background.png")

#캐릭터(스프라이트) 불러오기
character = pygame.image.load("C:\\Users\\pc\\Desktop\\python\\PythonGameClone1\\pygame_basic\\character.png")
character_size = character.get_rect().size # 이미지 크기 구해오기
character_width = character_size[0] #캐릭터 가로크기 0번째에 들어가있음
character_height = character_size[1] #캐릭터 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로의 절반크기 위치
character_y_pos = screen_height - character_height #화면 세로크기 가장아래

#이동할 좌표
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

#이동속도
character_speed = 0.5

# 적군
enemies = []
enemy = pygame.image.load("C:\\Users\\pc\\Desktop\\python\\PythonGameClone1\\pygame_basic\\enemy.png")
enemy_size = enemy.get_rect().size # 이미지 크기 구해오기
enemy_width = enemy_size[0] #캐릭터 가로크기 0번째에 들어가있음
enemy_height = enemy_size[1] #캐릭터 세로크기
# enemy_x_pos = random.randint(0, screen_width - enemy_width) # x축 랜덤으로 생성
# enemy_y_pos = 0 # 가장 위에서 시작
enemy_speed = 0.3 # 내려오는 속도
spawn_interval = 3
next_spawn_time = spawn_interval

enemies.append({
    "x" : random.randint(0, screen_width - enemy_width),
    "y" : 0
})

#점수 
score = 0
score_font = pygame.font.Font(None,40)
enemy_dodged = 0

# 폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 60

# 시작 시간
start_ticks = pygame.time.get_ticks() # 시작 tick을 받아옴

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수 설정

    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임 진행중이 아님

        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: # 키보드 왼쪽 클릭
                character_to_x_LEFT -= character_speed # x를 왼쪽으로 5만큼 이동
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed

        if event.type == pygame.KEYUP: # 방향키를 때면 더이상 움직이지 않도록
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    character_x_pos += character_to_x_LEFT * dt + character_to_x_RIGHT * dt

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = screen_width - character_width

    
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과시간을 ms를 s 로 단위변환

    # 게임시간에 따른 똥 재생성 시간 단축
    spawn_interval = max(0.5, 3 - (elapsed_time // 5) * 0.4)

    # 똥 움직임
    for enemy_data in enemies:
        enemy_data["y"] += enemy_speed * dt

    #똥 재생성
    if elapsed_time >= next_spawn_time:
        enemies.append({
            "x": random.randint(0, screen_width - enemy_width),
            "y": 0
        })
        next_spawn_time += spawn_interval

    # 똥이 떨어지고 난후 기존 리스트에서 제거
    new_enemies = []
    for enemy_data in enemies:
        if enemy_data["y"] > screen_height:
            enemy_dodged += 1
        else:
            new_enemies.append(enemy_data)

    enemies = new_enemies

    #충돌처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
        
    for enemy_data in enemies: # 리스트내 모든똥들에대해 충돌처리 안해주면 나중에는 충돌이 안먹힘
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_data["x"]
        enemy_rect.top = enemy_data["y"]
        if character_rect.colliderect(enemy_rect):
            print("충돌했어요")
            print(f"score : {score} 점")
            running = False
            break  # 하나만 부딪혀도 바로 끝내기

    screen.blit(background, (0,0)) #배경그리기
    screen.blit(character,(character_x_pos, character_y_pos)) # 캐릭터 그리기

    # enemy 그리기
    for enemy_data in enemies:
        screen.blit(enemy, (enemy_data["x"], enemy_data["y"]))
    
    #시간 표시
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (0,0,0)) # 시간정보, True (안티알리아스?), 글자색상
    screen.blit(timer, (10,10))

    #점수 표시 / 시간에 따른 점수 추가 
    score = int(elapsed_time * 50) + (enemy_dodged * 500)
    score_display = score_font.render(f"Score : {score}", True, (0,0,0))
    screen.blit(score_display, (10,50))

    # 똥내려오는 속도 증가
    enemy_speed = 0.3 + (int(elapsed_time) // 10) * 0.1

    if total_time - elapsed_time <= 0:
        print("축하합니다!")
        print(f"score : {score} 점")
        running = False

    pygame.display.update() #게임화면 다시그리기

# 잠시 대기
pygame.time.delay(1000) # 1 초 정도 대기 후 종료

# pygame 종료
pygame.quit()