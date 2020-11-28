from textgenrnn import textgenrnn
import jamspell

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num_str", help="number of strings of hokku (int)",
                    type=int)
parser.add_argument("--num_poems", help="number of poems to generate (int)",
                    type=int)
parser.add_argument("--num_words", help="number of words in generated novel (int)",
                    type=int)
parser.add_argument("--novel_mode", help="flag to novel mode (bool)",
                    type=bool)


args = parser.parse_args()
num_str = args.num_str
num_poems = args.num_poems
num_words = args.num_words
novel_mode = args.novel_mode

corrector = jamspell.TSpellCorrector()
corrector.LoadLangModel('/home/mitya/PycharmProjects/text_gen/models/ru_small.bin')

textgen = textgenrnn('/home/mitya/PycharmProjects/text_gen/models/bashe_300.hdf5')

letters = "А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я"
letters = letters.lower()
letters = letters.split(',')


class Generate():

    def __init__(self, num_str: int, num_poems: int, num_words=None, letters=None):
        if letters is None:
            self.letters = letters
        if num_words is None:
            self.num_words = num_words
        self.num_str = num_str
        self.num_poems = num_poems


    @staticmethod
    def hokku_str(num_str):
        '''generate poem'''
        hokku = []
        for i in range(num_str):
            hokku.append(textgen.generate(return_as_list=True, temperature=1.0))

        while ([''] in hokku):
            hokku.remove([''])

        hokku = list(filter(None, hokku))

        hokku_str = ''.join(map(str, hokku))
        hokku_str = hokku_str.replace('[', '').replace(']', '').replace('    ', '')
        hokku_str = hokku_str.split("'")

        return hokku_str


    def delete_empty(self, letters, x):
        '''check list for emptyness'''
        for letter in letters:
            if letter in x:
                return True
            else:
                return False


    def generate_poems(self, num_poems, num_str):
        '''generate list of poems'''
        poems = [None]
        for i in range(num_poems):
            poems[i] = self.hokku_str(num_str)
            poems.append(poems[i])
        return poems


    def filter_empty(self, poems):
        '''filter empty lists'''
        for i in range(len(poems)):
            poems[i] = [element for element in poems[i] if self.delete_empty(letters, element) == True]
        return poems


    def correct(self, poems):
        for i in range(len(poems)):
            for j in range(len(poems[i])):
                poems[i][j] = corrector.FixFragment(str(poems[i][j]))
        return poems


    def generate_end(self):
        '''pipeline to generate list of poems'''
        text = self.generate_poems(num_poems, num_str)
        result = self.filter_empty(text)
        result = self.correct(result)
        return result


    @staticmethod
    def list2string(s):
        str1 = " "
        return (str1.join(s))


    def count_words(self, text):
        b = 0
        for i in range(len(text)):
            a = len(self.list2string(text[i]).split())
            b += a
        return b


    def count_words_cmplx(self, text):
        c = 0
        for i in range(len(text)):
            e = self.count_words(text[i])
            c += e
        return c


    def generate_novel(self, limit=num_words):
        '''generate poems up until some limit in words'''
        text = []
        n_words = 0
        while True:
            # text[i] = generate_end()
            text.append(self.generate_end())
            n_words = self.count_words_cmplx(text)

            if n_words > limit:
                break
        return text


if __name__ == "__main__":
    if novel_mode:
        generate = Generate(num_str, num_poems, num_words)
        text = generate.generate_novel()
        print(text)
    else:
        generate = Generate(num_str, num_poems)
        text = generate.generate_end()
        print(text)
