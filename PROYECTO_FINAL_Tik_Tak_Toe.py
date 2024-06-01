import tkinter as tk
import random
import graphviz

class TicTacToe:
    def __init__(self, root, learning_agent, history, show_main_menu):
        self.root = root
        self.learning_agent = learning_agent
        self.history = history
        self.show_main_menu = show_main_menu
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.buttons = []
        self.create_board()
        self.reset_game()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=' ', font=('Arial', 20), width=5, height=2,
                               command=lambda i=i: self.handle_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def reset_game(self):
        for button in self.buttons:
            button.config(text=' ', state=tk.NORMAL, bg='SystemButtonFace')
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def handle_click(self, index):
        if self.board[index] == ' ':
            self.board[index] = 'X'
            self.buttons[index].config(text='X', disabledforeground='blue')
            if self.check_winner('X'):
                self.end_game('X')
            else:
                self.learning_agent.move(self)
                if self.check_winner('O'):
                    self.end_game('O')
                elif ' ' not in self.board:
                    self.end_game('Empate')

    def check_winner(self, letter):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]
        for combo in winning_combinations:
            if all(self.board[i] == letter for i in combo):
                self.current_winner = letter
                for i in combo:
                    self.buttons[i].config(bg='lightgreen')
                return True
        return False

    def end_game(self, winner):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.learning_agent.learn(self.board, winner)
        if winner != 'Empate':
            self.history.append(f"Ganador: {winner}")
        else:
            self.history.append("Empate")

        result_text = f"Resultado: {winner}"
        self.show_end_game_dialog(result_text)

    def show_end_game_dialog(self, result_text):
        result_dialog = tk.Toplevel(self.root)
        result_dialog.title("Fin del Juego")
        tk.Label(result_dialog, text=result_text, font=('Arial', 20), bg='lightyellow').pack(pady=10, padx=10)
        tk.Button(result_dialog, text="Jugar de Nuevo", command=lambda: [self.reset_game(), result_dialog.destroy()]).pack(pady=5)
        tk.Button(result_dialog, text="Regresar al Menú", command=lambda: [self.show_main_menu(), result_dialog.destroy()]).pack(pady=5)


class LearningAgent:
    def __init__(self):
        self.q_table = {}

    def move(self, game):
        empty_spots = [i for i, spot in enumerate(game.board) if spot == ' ']
        move = random.choice(empty_spots)
        game.board[move] = 'O'
        game.buttons[move].config(text='O', disabledforeground='red')

    def learn(self, board, winner):
        state = tuple(board)
        if state not in self.q_table:
            self.q_table[state] = {'X': 0, 'O': 0}
        if winner in self.q_table[state]:
            self.q_table[state][winner] += 1


class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tik Tak Toe")
        self.learning_agent = LearningAgent()
        self.history = []

    def run(self):
        self.show_main_menu()
        self.root.mainloop()

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Tik Tak Toe", font=('Arial', 24)).pack(pady=10)
        tk.Button(self.root, text="Jugar", command=self.start_game, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Historial", command=self.show_history, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Visualizar Aprendizaje", command=self.visualize_learning, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Integrantes", command=self.show_team, width=20, height=2).pack(pady=5)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        TicTacToe(self.root, self.learning_agent, self.history, self.show_main_menu)

    def show_history(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Historial de Partidas", font=('Arial', 24)).pack(pady=10)
        history_text = "\n".join(self.history)
        tk.Label(self.root, text=history_text, font=('Arial', 14)).pack(pady=10)

        scores = self.calculate_scores()
        if scores:
            max_score_player = max(scores, key=scores.get)
            max_score = scores[max_score_player]
            score_text = f"Jugador con más victorias: {max_score_player} ({max_score} victorias)"
            tk.Label(self.root, text=score_text, font=('Arial', 14)).pack(pady=10)

        tk.Button(self.root, text="Volver", command=self.show_main_menu, width=20, height=2).pack(pady=20)

    def calculate_scores(self):
        scores = {'X': 0, 'O': 0, 'Empate': 0}
        for result in self.history:
            if "Ganador: X" in result:
                scores['X'] += 1
            elif "Ganador: O" in result:
                scores['O'] += 1
            elif "Empate" in result:
                scores['Empate'] += 1
        return scores

    def visualize_learning(self):
        visualize_q_table(self.learning_agent.q_table)
        tk.Label(self.root, text="Visualización generada", font=('Arial', 24)).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.show_main_menu, width=20, height=2).pack(pady=20)

    def show_team(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Integrantes del Grupo", font=('Arial', 24)).pack(pady=10)
        tk.Label(self.root, text="Nombre: Abrahan Jucup Alvarado\nCarnet: 9490-1474\nSección: B", font=('Arial', 14)).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.show_main_menu, width=20, height=2).pack(pady=20)


def visualize_q_table(q_table):
    dot = graphviz.Digraph(comment='Q-Table')

    for state, actions in q_table.items():
        state_str = ''.join(state)
        dot.node(state_str, state_str)
        for action, value in actions.items():
            action_str = 'Ganador: ' + action if action != ' ' else 'Empate'
            dot.edge(state_str, action_str, label=str(value))

    dot.render('q_table.gv', view=True)


if __name__ == "__main__":
    menu = Menu()
    menu.run()
