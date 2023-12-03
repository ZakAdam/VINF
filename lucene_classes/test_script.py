from lucene_classes.query_class import LuceneSearcher
from lucene_classes.indexer_class import LuceneIndexer
import unittest
import lucene

# init Lucene
lucene.initVM()


class TestIndexSearch(unittest.TestCase):

    # Test number 1.
    def tests_results(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, test_env=True)
        results = lucene_searcher.query_string('Avdiivka')

        for result in results['UKR']:
            self.assertIn('Avdiivka', result['content'])

        for result in results['RUS']:
            self.assertIn('Avdiivka', result['content'])

    # Test number 2.
    def test_number_of_results(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, test_env=True)
        results = lucene_searcher.query_string('Avdiivka')

        self.assertEqual(len(results['UKR']), 10)

    # Test number 3.
    def test_only_ukr(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, test_env=True)
        results = lucene_searcher.query_string('Kosice')

        self.assertGreater(len(results['UKR']), 0)
        self.assertEqual(len(results['RUS']), 0)

    # Test number 4.
    def test_only_rus(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, test_env=True)
        results = lucene_searcher.query_string('Kvyat')

        self.assertGreater(len(results['RUS']), 0)
        self.assertEqual(len(results['UKR']), 0)

    # Test number 5.
    def test_empty_input(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, test_env=True)
        results = lucene_searcher.query_string('')

        self.assertIsNone(results, 'Empty input should get empty response')

    # Test number 6.
    def test_wiki_data_enabled(self):
        lucene_searcher = LuceneSearcher('wiki_index', 10, show_content='yes', test_env=True)
        results = lucene_searcher.query_string('Zuzana')

        for result in results['UKR']:
            self.assertIsNotNone(result['wiki_data'])

        for result in results['RUS']:
            self.assertIsNotNone(result['wiki_data'])

    # Test number 7.
    def test_date_search(self):
        lucene_searcher = LuceneSearcher('wiki_index', 3, test_env=True)
        results = lucene_searcher.query_string('2023_January_16', date_search=True)

        for result in results['UKR']:
            self.assertEqual('2023_January_16', result['date'])

        for result in results['RUS']:
            self.assertEqual('2023_January_16', result['date'])

    # Test number 8.
    def test_everything(self):
        lucene_searcher = LuceneSearcher('wiki_index', 3, show_content='yes', test_env=True)
        results = lucene_searcher.query_string('T-72')

        for result in results['UKR']:
            self.assertIn('T-72', result['content'])
            self.assertIsNotNone(result['wiki_data'])
            self.assertEqual('Ukraine', result['country'])

        for result in results['RUS']:
            self.assertIn('T-72', result['content'])
            self.assertIsNotNone(result['wiki_data'])
            self.assertEqual('Russia', result['country'])


if __name__ == '__main__':
    unittest.main()
