import sys

valid_coins = [5, 10, 20, 50, 100, 200]

class State():
    def __init__(self):
        self.lifter = False
        self.coins = 0

state = State()

for line in sys.stdin:
    line = line.lower().strip()
    
    if line.startswith("levantar"):
        if state.lifter:
            print("O telefone já está em uso.")
        else:
            state.lifter = True
            print("Introduzir moedas.")
            
    elif line.startswith("pousar"):
        if not state.lifter:
            print("O telefone não está em uso.")
        else:
            state.lifter = False
            change = []
            while state.coins > 0:
                for coin in reversed(valid_coins):
                    if state.coins >= coin:
                        state.coins -= coin
                        change.append(coin)
                        break
            
            # print coins in change list
            print("Troco: ", end="")
            for coin in change:
                if coin >= 100:
                    print("{}e".format(coin // 100), end="")
                print("{}c".format(coin % 100), end=" ")
            print()
            
    elif line.startswith("moeda"):
        invalid_coins = []
        
        for coin in line[5:].split(","):
            try:
                coin = int(coin.replace("c", "").replace("e", "00"))
                if coin in valid_coins:
                    state.coins += coin
                else:
                    invalid_coins.append(coin)
            except ValueError:
                invalid_coins.append(coin)
        if invalid_coins:
            print("Moedas inválidas: {}".format(", ".join(map(str, invalid_coins))))
        print("Saldo atual: {}c".format(state.coins))
        
    elif line.startswith("t="):
        if not state.lifter:
            print("O telefone não está em uso.")
            continue
        
        line = line[2:]
        
        if line.startswith("601") or line.startswith("641"):
            print("Chamada bloqueada")
        elif line.startswith("00"):
            if state.coins >= 150:
                state.coins -= 150
                print("Novo saldo: {}e{}c".format(state.coins // 100, state.coins % 100))
            else:
                print("Saldo insuficiente")
        elif len(line) == 9:
            if line.startswith("2"):
                if state.coins >= 25:
                    state.coins -= 25
                    print("Novo saldo: {}e{}c".format(state.coins // 100, state.coins % 100))
                else:
                    print("Saldo insuficiente")
            elif line.startswith("800"):
                print("Novo saldo: {}c".format(state.coins))
            elif line.startswith("808"):
                if state.coins >= 10:
                    state.coins -= 10
                    print("Novo saldo: {}e{}c".format(state.coins // 100, state.coins % 100))
                else:
                    print("Saldo insuficiente")
    
    elif line == "abortar":
        print("Até à próxima!")
        sys.exit(0)