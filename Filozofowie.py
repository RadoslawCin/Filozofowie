# Problem ucztujących filozofów to klasyczny problem synchronizacji w informatyce.
# W tym problemie, pięciu filozofów siedzi przy okrągłym stole, z talerzami przed nimi,
# a widelcami między nimi. Pomiędzy każdymi dwoma filozofami znajduje się jeden widelec.
# Filozofowie mają tylko dwie czynności: jedzenie i myślenie. Kiedy filozof jest głodny,
# próbuje podnieść dwa widelce znajdujące się obok niego, a następnie jeść. Po zakończeniu
# posiłku odkłada widelce i wraca do myślenia.

# Poniżej użyto kelnera do rozwiązania problemu. Kelner jest świadomy które widelce są w użyciu

import threading
import time
from colorama import init, Fore, Style

init(autoreset=True)

colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA]
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_MAGENTA = "\033[95m"
COLOR_RESET = "\033[0m"


class Kelner:
    def __init__(self, liczba_filozofow, imiona_filozofow):
        self.lock = threading.Lock()
        self.dostepne_widelce = [True] * liczba_filozofow
        self.statystyki = {imie: {'jedzenie': 0, 'oczekiwanie': 0, 'podnoszenie': 0, 'odkladanie': 0} for imie in
                           imiona_filozofow}

    def podnies_widelce(self, filozof, imie):
        self.lock.acquire()
        while not self.dostepne_widelce[filozof] or not self.dostepne_widelce[
            (filozof + 1) % len(self.dostepne_widelce)]:
            self.lock.release()
            with print_lock:
                print(f"{colors[filozof]}{imie}{Style.RESET_ALL} czeka na wolne widelce.")
            self.statystyki[imie]['oczekiwanie'] += 1
            time.sleep(0.5)
            self.lock.acquire()

        self.dostepne_widelce[filozof] = False
        self.dostepne_widelce[(filozof + 1) % len(self.dostepne_widelce)] = False
        with print_lock:
            print(f"{colors[filozof]}{imie}{Style.RESET_ALL} podniósł widelce.")
        self.statystyki[imie]['podnoszenie'] += 1
        self.lock.release()

    def odloz_widelce(self, filozof, imie):
        self.lock.acquire()
        self.dostepne_widelce[filozof] = True
        self.dostepne_widelce[(filozof + 1) % len(self.dostepne_widelce)] = True
        with print_lock:
            print(f"{colors[filozof]}{imie}{Style.RESET_ALL} odłożył widelce.")
        self.statystyki[imie]['odkladanie'] += 1
        self.lock.release()


class Filozof(threading.Thread):
    def __init__(self, kelner, numer, imie):
        threading.Thread.__init__(self)
        self.kelner = kelner
        self.numer = numer
        self.imie = imie
        self.running = True

    def run(self):
        while self.running:
            self.myśl()
            self.jedz()

    def myśl(self):
        with print_lock:
            print(f"{colors[self.numer]}{self.imie}{Style.RESET_ALL} myśli.")
        self.kelner.statystyki[self.imie]['oczekiwanie'] += 1
        time.sleep(1)  # Symulacja myślenia

    def jedz(self):
        self.kelner.podnies_widelce(self.numer, self.imie)
        with print_lock:
            print(f"{colors[self.numer]}{self.imie}{Style.RESET_ALL} je.")
        self.kelner.statystyki[self.imie]['jedzenie'] += 1
        time.sleep(1)  # Symulacja jedzenia
        self.kelner.odloz_widelce(self.numer, self.imie)


if __name__ == "__main__":
    liczba_filozofow = 5
    imiona_filozofow = ["Aristoteles", "Platon", "Sokrates", "Epikur", "Heraklit"]

    kelner = Kelner(liczba_filozofow, imiona_filozofow)
    filozofowie = []

    print_lock = threading.Lock()

    for i in range(liczba_filozofow):
        filozof = Filozof(kelner, i, imiona_filozofow[i])
        filozofowie.append(filozof)

    for filozof in filozofowie:
        filozof.start()

    time.sleep(60)  # Czas trwania obiadu (1 minuta)

    for filozof in filozofowie:
        filozof.running = False

    for filozof in filozofowie:
        filozof.join()

    print(COLOR_RED + "\nObiad został zakończony.\n" + COLOR_RESET)
    print("Podsumowanie statystyk:\n")
    for imie, statystyki in kelner.statystyki.items():
        print(f"Filozof {colors[imiona_filozofow.index(imie)]}{imie}{Style.RESET_ALL}:\n")
        print(COLOR_YELLOW + f"  Jedzenie: {statystyki['jedzenie']} razy" + COLOR_RESET)
        print(COLOR_GREEN + f"  Oczekiwanie: {statystyki['oczekiwanie']} razy" + COLOR_RESET)
        print(COLOR_RED + f"  Podnoszenie widelców: {statystyki['podnoszenie']} razy" + COLOR_RESET)
        print(COLOR_MAGENTA + f"  Odkładanie widelców: {statystyki['odkladanie']} razy\n" + COLOR_RESET)
