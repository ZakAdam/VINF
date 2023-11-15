from lucene_classes.query_class import LuceneSearcher


class ConsoleLuceneSearch:
    def __init__(self):
        self.lucene_searcher = LuceneSearcher('index')

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-3, or 'q' to quit): ").lower()

            if choice == '1':
                search_string = input("Enter the search string: ")
                self.lucene_searcher.query_string(search_string)
            elif choice == 'q':
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def display_menu(self):
        print("\nLucene Search Console")
        print("1. Perform Search")
        print("q. Quit")


if __name__ == "__main__":
    console_app = ConsoleLuceneSearch()
    console_app.run()
