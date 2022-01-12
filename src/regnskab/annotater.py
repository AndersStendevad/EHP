from simple_term_menu import TerminalMenu
import os
import textwrap
def progress(count, total):
    bar_len = 280//5-6
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    return f"[{bar}]{percents}%\n line {count} out of {total} lines"

class Annotater:

    def __init__(self, total = None):
        self.total = total
        self.count = 0
        try:
            self._tags = []
            with open("tags.txt", "r") as file:
                for tag in file.readlines():
                    if tag:
                        self._tags.append(tag.strip())
        except FileNotFoundError:
            self._tags = ["1.done", "2.new_tag"]

    def annotate(self, tweet):
        tags = self._annotate(tweet)
        return list(set(tags))

    def _annotate(self, tweet):
        os.system('cls' if os.name == 'nt' else 'clear')
        title = ""
        if self.total:
            title += progress(self.count, self.total)+"\n"
        chunk_size = 280//5
        title += ":"*chunk_size+"\n"+textwrap.fill(tweet, chunk_size)+"\n"+":"*chunk_size
        terminal_menu = TerminalMenu(self._tags, search_key=None, title=title)

        try:
            choice_index = terminal_menu.show()
        except ValueError:
            return self.annotate(tweet)

        if choice_index is not None:
            choice = self._tags[choice_index]
            if choice == "1.done":
                return []
            elif choice == "2.new_tag":
                try:
                    new_tag = input("Name of new tag: ")
                except KeyboardInterrupt:
                    return self.annotate(tweet)
                if not new_tag:
                    return self.annotate(tweet)
                os.system('cls' if os.name == 'nt' else 'clear')
                if new_tag not in self._tags:
                    self._tags.append(new_tag)
                return [new_tag] + self.annotate(tweet)
            else:
                return [choice] + self.annotate(tweet)


        else:
            terminal_menu = TerminalMenu(["continue","exit"], search_key=None)
        choice_index = terminal_menu.show()
        if choice_index is None or choice_index == 1:
            with open("tags.txt", "w+") as file:
                for tag in self._tags:
                    file.write(f"{tag}\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        else:
            return self.annotate(tweet)
    def save_tags(self):
        with open("tags.txt", "w+") as file:
            for tag in self._tags:
                file.write(f"{tag}\n")
        exit()

