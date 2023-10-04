import tkinter as tk
import random

class PongGame:
    def __init__(self, master, width=400, height=300):
        self.master = master
        self.master.title("Ping Pong Game")
        self.width = width
        self.height = height

        # Ustawienia piłki
        self.ball_size = 15
        self.ball_speed = 5
        self.ball = {'x': width // 2, 'y': height // 2, 'dx': 1, 'dy': 1}

        # Ustawienia paletki
        self.paddle_width = 50
        self.paddle_height = 10
        self.paddle = {'x': width // 2 - self.paddle_width // 2, 'y': height - self.paddle_height}

        # Wynik
        self.score = 0

        # Stan gry
        self.game_running = False

        # Utworzenie Canvas
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Etykieta wyniku
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 12), fg="white", bg="black")
        self.score_label.pack()

        # Przycisk startu
        self.start_button = tk.Button(self.master, text="Start Gry", command=self.start_game)
        self.start_button.pack()

        # Przycisk restartu
        self.restart_button = tk.Button(self.master, text="Restart", command=self.reset_game, state=tk.DISABLED)
        self.restart_button.pack()

        # Obsługa klawiszy
        self.master.bind("<Left>", self.move_paddle_left)
        self.master.bind("<Right>", self.move_paddle_right)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.start_button.pack_forget()
            self.restart_button.config(state=tk.NORMAL)
            self.move_ball()

    def move_ball(self):
        if self.game_running:
            self.ball['x'] += self.ball_speed * self.ball['dx']
            self.ball['y'] += self.ball_speed * self.ball['dy']

            # Odbicie od ścian
            if self.ball['x'] <= 0 or self.ball['x'] >= self.width - self.ball_size:
                self.ball['dx'] = -self.ball['dx']

            # Odbicie od paletki (tylko od góry)
            if (
                self.paddle['x'] <= self.ball['x'] <= self.paddle['x'] + self.paddle_width and
                self.paddle['y'] <= self.ball['y'] <= self.paddle['y'] + self.paddle_height and
                self.ball['dy'] > 0  # Odbicie tylko gdy piłka porusza się w dół
            ):
                self.ball['dy'] = -self.ball['dy']
                self.score += 1
                self.ball_speed += 0.5  # Zwiększenie prędkości piłki
                self.update_score()

            # Odbicie od góry
            if self.ball['y'] <= 0:
                self.ball['dy'] = -self.ball['dy']

            # Odbicie od dołu
            if self.ball['y'] >= self.height:
                self.game_over()

            # Rysowanie piłki i paletki
            self.canvas.delete("all")
            self.canvas.create_rectangle(self.paddle['x'], self.paddle['y'],
                                         self.paddle['x'] + self.paddle_width, self.paddle['y'] + self.paddle_height,
                                         fill="white")
            self.canvas.create_oval(self.ball['x'], self.ball['y'],
                                    self.ball['x'] + self.ball_size, self.ball['y'] + self.ball_size,
                                    fill="white")

            # Aktualizacja ekranu
            self.master.after(20, self.move_ball)

    def move_paddle_left(self, event):
        if self.paddle['x'] > 0:
            self.paddle['x'] -= 10

    def move_paddle_right(self, event):
        if self.paddle['x'] < self.width - self.paddle_width:
            self.paddle['x'] += 10

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", font=("Helvetica", 16), fill="red")
        self.restart_button.config(state=tk.NORMAL)

    def reset_game(self):
        self.game_running = False
        self.start_button.pack()
        self.restart_button.config(state=tk.DISABLED)
        self.ball_speed = 5
        self.ball['x'] = self.width // 2
        self.ball['y'] = self.height // 2
        self.ball['dx'] = random.choice([-1, 1])
        self.ball['dy'] = random.choice([-1, 1])
        self.score = 0
        self.update_score()

if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
