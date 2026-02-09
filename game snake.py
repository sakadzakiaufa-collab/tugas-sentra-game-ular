import tkinter
import random  

ROWS = 25
COLS = 25
TILE_SIZE = 30

WINDOW_WIDTH = TILE_SIZE * COLS  
WINDOW_HEIGHT = TILE_SIZE * ROWS  

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="blue", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/3) - (window_width/3))
window_y = int((screen_height/3) - (window_height/3))

# Format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Load apple image for food (pastikan file apple.png ada di direktori yang sama)
try:
    apple_img = tkinter.PhotoImage(file="apple.png").subsample(2, 2)  # Resize jika perlu, sesuaikan subsample
except:
    apple_img = None  # Jika gambar tidak ada, gunakan rectangle merah sebagai fallback

# Initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)  # Single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = []  # Multiple snake tiles
game_over = False
score = 0
lives = 3  # Tambahan: 3 nyawa

# Game loop
def change_direction(e):  # e = event
    global velocityX, velocityY, game_over, snake, snake_body, food, score, lives
    if game_over:
        if lives > 0:
            # Reset game jika nyawa masih ada
            snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
            snake_body = []
            food.x = random.randint(0, COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE
            velocityX = 0
            velocityY = 0
            game_over = False
            lives -= 1  # Kurangi nyawa
        return

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, lives
    if game_over:
        return
    
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return
    
    # Collision with food
    if snake.x == food.x and snake.y == food.y: 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    # Update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score, lives
    move()

    canvas.delete("all")

    # Draw food as apple image (or red rectangle if image not found)
    if apple_img:
        canvas.create_image(food.x + TILE_SIZE//2, food.y + TILE_SIZE//2, image=apple_img)
    else:
        canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw snake as more realistic shape (head as oval, body as smaller ovals)
    # Head: Oval hijau, sedikit lebih besar
    head_x1 = snake.x + 2
    head_y1 = snake.y + 2
    head_x2 = snake.x + TILE_SIZE - 2
    head_y2 = snake.y + TILE_SIZE - 2
    canvas.create_rectangle(head_x1, head_y1, head_x2, head_y2, fill='lime green', outline='dark green')

    # Body: Oval yang lebih kecil dan gelap
    for tile in snake_body:
        body_x1 = tile.x + 4
        body_y1 = tile.y + 4
        body_x2 = tile.x + TILE_SIZE - 4
        body_y2 = tile.y + TILE_SIZE - 4
        canvas.create_rectangle(body_x1, body_y1, body_x2, body_y2, fill='dark green', outline='black')

    if game_over:
        if lives == 0:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over! Final Score: {score}", fill="white")
        else:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20, font="Arial 20", text=f"Game Over! Lives Left: {lives}", fill="white")
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20, font="Arial 15", text="Press Arrow Key to Continue", fill="white")
    else:
        canvas.create_text(
            60, 20, 
            font="Arial 10", 
            text=f"Score: {score} | Lives: {lives}", 
            fill="white"
        )
    
    window.after(100, draw)  # Call draw again every 100ms (10 FPS)

draw()
window.bind("<KeyRelease>", change_direction)  # When you press any key and release
window.mainloop()  # Listen to window events