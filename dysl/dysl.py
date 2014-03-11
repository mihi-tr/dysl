import sys
import codecs

from dyslib.lm import LM

# Corpora should have their own libs 
sys.path.append('../corpora')

corpora = {
    'English': '../corpora/corpus-5langs/en.txt',
    'Spanish': '../corpora/corpus-5langs/es.txt',
    'French': '../corpora/corpus-5langs/fr.txt',
    'Arabic': '../corpora/corpus-5langs/ar.txt',
    'Arabizi': '../corpora/corpus-5langs/ar-latin.txt',
}

def term2ch(text):
    return [ch for ch in text]


def readfile(filename):
    #print 'readfile', filename
    f = codecs.open(filename, encoding='utf-8')
    tokenz = term2ch(f.read())
    f.close()
    #print tokenz
    return tokenz


class MyLM(LM):

    def classify(self, text=u''):
        result = self.calculate(doc_terms=term2ch(text))
        return (result['calc_id'], 0)

def main_cli():
    
    ngram = 3
    lrpad = u' '
    verbose=True

    lm = LM(n=ngram, verbose=verbose, lpad=lrpad, rpad=lrpad, 
            smoothing='Laplace', laplace_gama=0.1, 
            corpus_mix='l')

    for lang in corpora:
        print 'Training on language,', lang
        lm.add_doc(doc_id=lang, doc_terms=readfile(corpora[lang]))

    intxt = u''
    for u in sys.argv[1:]:
        intxt = intxt + u.decode('utf-8')
    
    print term2ch(intxt)
    result = lm.calculate(doc_terms=term2ch(intxt))
    print result['calc_id']

def main_esaren():

    ngram = 3
    lrpad = u' '
    verbose=False

    lm = MyLM(n=ngram, verbose=verbose, lpad=lrpad, rpad=lrpad, 
            smoothing='Laplace', laplace_gama=0.1, 
            corpus_mix='l')

    import corpuslib
    train = corpuslib.Train()
    corpus = train.get_corpus()

    for item in corpus:
        lm.add_doc(doc_id=item[0], doc_terms=readfile(item[1]))

    a = corpuslib.Accuracy()
    t = corpuslib.Test(root='', langid=lm, accuracy=a)
    t.start()
    a.evaluate()


if __name__ == '__main__':

    PROFILING = False

    if PROFILING:
        import cProfile
        import pstats

    # For an interactive mode
    #main_cli()

    # For training and testing esaren corpus
    if PROFILING:
        cProfile.run('main_esaren()','train_prof')
        p_stats = pstats.Stats('train_prof')
        p_stats.sort_stats('time').print_stats(10)
    else:
        main_esaren()

