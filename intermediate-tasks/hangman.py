"""
ShadowFox Internship - Task 2: Hangman Game
============================================
Features:
  - Visual ASCII gallows (7 stages)
  - 4 difficulty levels: Easy / Medium / Hard / Expert
  - Smart hint system (unlocks after 3 wrong guesses)
  - ANSI color output
  - 5 word categories with curated word banks
  - Score tracking across multiple rounds
"""

import random, os, sys

def supports_color():
    return hasattr(sys.stdout,"isatty") and sys.stdout.isatty()

USE_COLOR = supports_color()
def c(code, t): return f"\033[{code}m{t}\033[0m" if USE_COLOR else t
RED     = lambda t: c("91", t)
GREEN   = lambda t: c("92", t)
YELLOW  = lambda t: c("93", t)
CYAN    = lambda t: c("96", t)
MAGENTA = lambda t: c("95", t)
BOLD    = lambda t: c("1",  t)
DIM     = lambda t: c("2",  t)

WORD_BANK = {
    "Science":    {"easy":["atom","gene","acid","cell","mass"],
                   "medium":["photon","neutron","plasma","enzyme","osmosis"],
                   "hard":["mitochondria","photosynthesis","thermodynamics","chromosomes"],
                   "expert":["bioluminescence","superconductivity","electrochemistry"]},
    "Technology": {"easy":["byte","code","data","loop","file"],
                   "medium":["kernel","python","server","docker","binary"],
                   "hard":["algorithm","blockchain","cryptography","microservice"],
                   "expert":["containerization","parallelization","asynchronous"]},
    "Animals":    {"easy":["bear","frog","wolf","duck","deer"],
                   "medium":["jaguar","falcon","walrus","coyote","badger"],
                   "hard":["chameleon","wolverine","platypus","crocodile"],
                   "expert":["archaeopteryx","hippopotamus","tyrannosaurus"]},
    "Geography":  {"easy":["nile","alps","asia","peru","iraq"],
                   "medium":["amazon","sahara","mongolia","iceland","pacific"],
                   "hard":["kilimanjaro","mesopotamia","madagascar","antarctica"],
                   "expert":["mediterranean","himalayan","appalachian"]},
    "Movies":     {"easy":["jaws","cars","troy","thor","dune"],
                   "medium":["avatar","shrek","matrix","titanic","batman"],
                   "hard":["inception","gladiator","parasite","interstellar"],
                   "expert":["cinematography","extraterrestrial","apocalyptic"]},
}

HINTS = {
    "Science":    "This is a science / biology / physics term.",
    "Technology": "This is a computing or software term.",
    "Animals":    "This is the name of an animal.",
    "Geography":  "This is a place, landmark, or geographic feature.",
    "Movies":     "This is a well-known movie title or film term.",
}

GALLOWS = [
    ["  +---+  ","  |   |  ","         ","         ","         ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","         ","         ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","  |   |  ","         ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","  |  /|  ","         ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","  |  /|\\ ","         ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","  |  /|\\ ","  |  /   ","         ","========="],
    ["  +---+  ","  |   |  ","  |   O  ","  |  /|\\ ","  |  / \\ ","         ","========="],
]
MAX_WRONG = 6

class HangmanGame:
    def __init__(self, word, category, difficulty):
        self.word=word.lower(); self.category=category; self.difficulty=difficulty
        self.guessed=set(); self.wrong=[]; self.hint_used=False; self.hint_revealed=False

    @property
    def wrong_count(self): return len(self.wrong)
    @property
    def won(self): return all(c in self.guessed for c in self.word)
    @property
    def lost(self): return self.wrong_count >= MAX_WRONG
    @property
    def done(self): return self.won or self.lost

    def display_word(self):
        return " ".join(
            (BOLD(GREEN(ch)) if ch in self.guessed else (YELLOW("_") if ch.isalpha() else ch))
            for ch in self.word)

    def guess(self, letter):
        letter=letter.lower()
        if letter in self.guessed or letter in self.wrong: return "already"
        if letter in self.word: self.guessed.add(letter); return "correct"
        self.wrong.append(letter); return "wrong"

    def reveal_hint_letter(self):
        pool=[ch for ch in self.word if ch not in self.guessed and ch.isalpha()]
        if pool:
            letter=random.choice(pool); self.guessed.add(letter)
            self.hint_revealed=True; return letter
        return None

def clr(): os.system("cls" if os.name=="nt" else "clear")

def banner():
    print(BOLD(CYAN("  ╔══════════════════════════════════════╗")))
    print(BOLD(CYAN("  ║   H A N G M A N  —  ShadowFox        ║")))
    print(BOLD(CYAN("  ╚══════════════════════════════════════╝")))

def draw_gallows(n):
    stage=GALLOWS[n]
    for i,row in enumerate(stage):
        if n>=6 and i in (2,3,4): print("  "+RED(BOLD(row)))
        elif n>=1 and i==2: print("  "+YELLOW(row))
        else: print("  "+CYAN(row))

def print_state(game, score):
    print()
    print(f"  {DIM('Score:')} {GREEN(str(score['wins']))} wins  {RED(str(score['losses']))} losses  "
          f"{DIM('|')}  {CYAN(game.category)}  {MAGENTA(game.difficulty.capitalize())}")
    print()
    draw_gallows(game.wrong_count)
    rem=MAX_WRONG-game.wrong_count
    print(f"\n  Lives: [{RED('#'*game.wrong_count)}{GREEN('-'*rem)}] {RED(str(game.wrong_count))}/{MAX_WRONG}")
    print(f"\n  Word:  {game.display_word()}")
    print(f"         ({len(game.word)} letters)\n")
    if game.wrong:
        print(f"  Wrong: {' '.join(RED(l.upper()) for l in game.wrong)}")
    else:
        print(f"  Wrong: {DIM('none yet')}")
    correct=[ch for ch in game.guessed if ch in game.word]
    if correct:
        print(f"  Found: {' '.join(GREEN(l.upper()) for l in sorted(correct))}")
    if not game.hint_revealed:
        until=3-game.wrong_count
        if until<=0: print(f"\n  {YELLOW('[H] Hint available! — type H')}")
        else: print(f"\n  {DIM(f'Hint unlocks in {until} more wrong guess(es)')}")
    print(f"\n  {DIM('Hint:')} {HINTS[game.category]}\n")

def choose_opt(prompt, opts):
    while True:
        ch=input(f"\n  {CYAN('>')} ").strip()
        if ch in opts: return opts[ch]
        print(RED(f"  Invalid. Choose: {', '.join(opts)}"))

def play_round(score):
    clr(); banner()
    print(BOLD("\n  Choose Difficulty:"))
    for k,v in [("1","easy"),("2","medium"),("3","hard"),("4","expert")]:
        desc={"easy":"4-5 letters","medium":"6-7 letters","hard":"8-10 letters","expert":"11+ letters"}[v]
        print(f"    [{k}] {v.capitalize():<8}  {DIM(desc)}")
    diff=choose_opt("", {"1":"easy","2":"medium","3":"hard","4":"expert"})

    clr(); banner()
    cats=list(WORD_BANK.keys())
    print(BOLD("\n  Choose Category:"))
    opts={}
    for i,cat in enumerate(cats,1):
        print(f"    [{i}] {cat}"); opts[str(i)]=cat
    print("    [6] Random"); opts["6"]=None
    ch=choose_opt("", opts)
    category=random.choice(cats) if ch is None else ch

    word=random.choice(WORD_BANK[category][diff])
    game=HangmanGame(word, category, diff)

    while not game.done:
        clr(); banner(); print_state(game, score)
        raw=input(f"  {BOLD('Guess')} (letter / H=hint / Q=quit): ").strip()
        if raw.lower()=="q":
            print(f"\n  {YELLOW('Quit!')} Word was: {BOLD(GREEN(game.word.upper()))}"); return
        if raw.lower()=="h":
            if game.wrong_count>=3 and not game.hint_revealed:
                letter=game.reveal_hint_letter()
                print(GREEN(f"  Hint: revealed '{letter.upper()}'"))
                game.hint_used=True
            elif game.hint_revealed: print(RED("  Hint already used!"))
            else: print(YELLOW(f"  Hint unlocks after 3 wrong guesses."))
            input(DIM("  [Enter]...")); continue
        if len(raw)!=1 or not raw.isalpha():
            print(RED("  Single letter only.")); input(DIM("  [Enter]...")); continue
        result=game.guess(raw)
        if result=="already": print(YELLOW(f"  Already guessed '{raw.upper()}'."))
        elif result=="correct": print(GREEN(f"  Correct! '{raw.upper()}' is in the word!"))
        else: print(RED(f"  Wrong! '{raw.upper()}' is not in the word."))
        if not game.done: input(DIM("  [Enter]..."))

    clr(); banner(); print_state(game, score)
    if game.won:
        score["wins"]+=1
        bonus=" (hint used)" if game.hint_used else ""
        print(GREEN(BOLD(f"\n  YOU WIN{bonus}! Word: {game.word.upper()}")))
        print(GREEN("  " + "* " * 12))
    else:
        score["losses"]+=1
        print(RED(BOLD(f"\n  GAME OVER! Word was: {game.word.upper()}")))
    again=input(f"\n  {BOLD('Play again?')} [y/n]: ").strip().lower()
    if again=="y": play_round(score)

def main():
    score={"wins":0,"losses":0}
    clr(); banner()
    print(f"""
  Welcome to Hangman!

  Rules:
    - Guess one letter at a time
    - {MAX_WRONG} wrong guesses = game over
    - Type H after 3 wrong guesses to reveal a hint letter
    - Type Q to quit the current round

  Categories: Science, Technology, Animals, Geography, Movies
  Difficulty: Easy | Medium | Hard | Expert
""")
    input(f"  {CYAN('Press Enter to start...')}")
    play_round(score)
    clr(); banner()
    total=score["wins"]+score["losses"]
    pct=score["wins"]/total*100 if total else 0
    print(f"\n  {BOLD('Final Score:')}")
    print(f"    {GREEN('Wins  :')} {score['wins']}")
    print(f"    {RED('Losses:')} {score['losses']}")
    print(f"    {CYAN('Win Rate:')} {pct:.0f}%")
    print(f"\n  {BOLD('Thanks for playing! — ShadowFox')}\n")

if __name__=="__main__":
    main()
