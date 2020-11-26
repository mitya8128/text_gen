from textgenrnn import textgenrnn
import jamspell

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num_str", help="number of strings of hokku",
                    type=int)
parser.add_argument("--num_poems", help="number of poems to generate",
                    type=int)

args = parser.parse_args()
num_str = args.num_str
num_poems = args.num_poems

corrector = jamspell.TSpellCorrector()
corrector.LoadLangModel('/home/mitya/PycharmProjects/text_gen/models/ru_small.bin')

textgen = textgenrnn('/home/mitya/PycharmProjects/text_gen/models/bashe_300.hdf5')

letters = "А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я"
letters = letters.lower()
letters = letters.split(',')


class Generate():

    def __init__(self, num_str: int, num_poems: int, letters=None):
        if letters is None:
            self.letters = letters
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
        text = self.generate_poems(num_poems, num_str)
        result = self.filter_empty(text)
        result = self.correct(result)
        return result


if __name__ == "__main__":
    # text = Generate.hokku_str(num_str)
    generate = Generate(num_str, num_poems)
    text = generate.generate_end()
    print(text)
