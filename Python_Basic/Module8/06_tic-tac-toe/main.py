# TODO здесь писать код
class Cell:
    def __init__(self, number):
        self.number = number
        self.symbol = ' '
        self.is_occupied = False

    def set_symbol(self, symbol):
        if not self.is_occupied:
            self.symbol = symbol
            self.is_occupied = True
            return True
        return False

class Board:
    def __init__(self):
        self.cells = [Cell(i) for i in range(1, 10)]

    def change_cell(self, cell_num, symbol):
        if 1 <= cell_num <= 9:
            return self.cells[cell_num - 1].set_symbol(symbol)
        return False

    def check_game_over(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # строки
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # столбцы
            [0, 4, 8], [2, 4, 6]               # диагонали
        ]
        for combo in win_combinations:
            if (self.cells[combo[0]].symbol == self.cells[combo[1]].symbol == self.cells[combo[2]].symbol
                    and self.cells[combo[0]].symbol != ' '):
                return True
        return False

    def is_full(self):
        return all(cell.is_occupied for cell in self.cells)

    def display(self):
        for i in range(0, 9, 3):
            row = [self.cells[i].symbol, self.cells[i+1].symbol, self.cells[i+2].symbol]
            print(' | '.join(row))
            if i < 6:
                print('---------')

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.wins = 0

    def make_move(self):
        while True:
            try:
                cell = int(input(f"{self.name}, введите номер клетки (1-9): "))
                if 1 <= cell <= 9:
                    return cell
                else:
                    print("Номер клетки должен быть от 1 до 9.")
            except ValueError:
                print("Для работы программы введите число.")

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.game_over = False

    def play_turn(self, player):
        self.board.display()
        cell = player.make_move()
        if self.board.change_cell(cell, player.symbol):
            if self.board.check_game_over():
                print(f"{player.name} победил!")
                player.wins += 1
                self.game_over = True
                return True
            elif self.board.is_full():
                print("Ничья!")
                self.game_over = True
                return True
        else:
            print("Клетка занята или неверный номер.")
        return False

    def play_one_game(self):
        self.board = Board()
        self.game_over = False
        current_player = self.player1
        while not self.game_over:
            if self.play_turn(current_player):
                break
            current_player = self.player2 if current_player == self.player1 else self.player1
        return True

    def start_games(self):
        while True:
            self.play_one_game()
            print(f"Счёт: {self.player1.name} — {self.player1.wins}, {self.player2.name} — {self.player2.wins}")
            again = input("Хотите сыграть ещё раз? (да/нет): ").lower()
            if again != 'да':
                break

# Пример использования
player1 = Player("Игрок 1", "X")
player2 = Player("Игрок 2", "O")
game = Game(player1, player2)
game.start_games()
