import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wasd=white, Arrow Keys=green, first to 5 wins")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 7

BALL_SIZE = 20
BALL_SPEED_X = 5 * random.choice((1, -1))
BALL_SPEED_Y = 5 * random.choice((1, -1))

player1_score = 0
player2_score = 0
FONT = pygame.font.Font(None, 74)

player1_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

game_over = False

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    BALL_SPEED_X = 5 * random.choice((1, -1))
    BALL_SPEED_Y = 5 * random.choice((1, -1))

def draw_elements():
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, WHITE, player1_paddle)
    pygame.draw.rect(SCREEN, GREEN, player2_paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    player1_text = FONT.render(str(player1_score), True, WHITE)
    player2_text = FONT.render(str(player2_score), True, WHITE)
    SCREEN.blit(player1_text, (WIDTH // 4, 20))
    SCREEN.blit(player2_text, (WIDTH * 3 // 4 - player2_text.get_width(), 20))

    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                game_over = False
                player1_score = 0
                player2_score = 0
                reset_ball()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player1_paddle.top > 0:
            player1_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player1_paddle.bottom < HEIGHT:
            player1_paddle.y += PADDLE_SPEED

        if keys[pygame.K_w] and player2_paddle.top > 0:
            player2_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player2_paddle.bottom < HEIGHT:
            player2_paddle.y += PADDLE_SPEED

        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1

        if ball.colliderect(player1_paddle):
            if abs(ball.left - player1_paddle.right) < 10 and BALL_SPEED_X < 0:
                BALL_SPEED_X *= -1

        if ball.colliderect(player2_paddle):
            if abs(ball.right - player2_paddle.left) < 10 and BALL_SPEED_X > 0:
                BALL_SPEED_X *= -1


        if ball.left <= 0:
            player2_score += 1
            reset_ball()
            if player2_score >= 5:
                game_over = True
        if ball.right >= WIDTH:
            player1_score += 1
            reset_ball()
            if player1_score >= 5:
                game_over = True

    draw_elements()

    if game_over:
        winner_text = ""
        if player1_score > player2_score:
            winner_text = "Player 1 Wins!"
        else:
            winner_text = "Player 2 Wins!"
        restart_text = "Press 'R' to Restart"

        winner_surface = FONT.render(winner_text, True, RED)
        restart_surface = FONT.render(restart_text, True, BLUE)

        winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        SCREEN.blit(winner_surface, winner_rect)
        SCREEN.blit(restart_surface, restart_rect)
        pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
