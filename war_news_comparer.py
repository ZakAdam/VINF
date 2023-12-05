from lucene_classes.query_class import LuceneSearcher  # Import LuceneSearcher class for querying
from lucene_classes.indexer_class import LuceneIndexer  # Import LuceneIndexer class for indexing
import lucene

# Define a class for a console-based Lucene search application
class ConsoleLuceneSearch:
    def __init__(self):
        lucene.initVM()  # Initialize Lucene VM

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-3, or 'q' to quit): ").lower()

            if choice == '1':
                # Option 1: Perform content search
                search_string = input("Enter the search string: ")
                number_of_results = input("Enter the number of results: ")
                show_content = bool(input("Show date events? (yes/no): "))
                lucene_searcher = LuceneSearcher('wiki_index', int(number_of_results), show_content)
                lucene_searcher.query_string(search_string)
            elif choice == '2':
                # Option 2: Create a new index
                index_name = input('Enter the new name of the created index: ')
                indexer = LuceneIndexer(index_name)
                indexer.index_csv()
            elif choice == '3':
                # Option 3: Perform date search
                search_string = input('Enter the date you want to find: ')
                number_of_results = input("Enter the number of results: ")
                show_content = bool(input("Show date events? (yes/no): "))
                lucene_searcher = LuceneSearcher('wiki_index', int(number_of_results), show_content)
                lucene_searcher.query_string(search_string, date_search=True)
            elif choice == 'q':
                # Option 'q': Quit the application
                break
            else:
                # Invalid choice
                print("Invalid choice. Please enter a valid option.")

    def display_menu(self):
        # Method to display the menu options
        print("\nLucene Search Console")
        print("1. Perform content Search")
        print("2. Create new Index")
        print("3. Perform date search")
        print("q. Quit")


# Run the console application if the script is executed directly
if __name__ == "__main__":
    console_app = ConsoleLuceneSearch()
    console_app.run()
