import requests
from bs4 import BeautifulSoup

WEBSITE = 'https://chemequations.com/en'
TO_DELETE = ('(aq)', '(l)', '(g)', '\xa0')

def remove_trash(text: str) -> str:
    for trash in TO_DELETE:
        text = text.replace(trash, '')
    return text.lower()
    


class Chemistry:
    def __init__(self) -> None:
        self.cache_reagents = []
        self.cache_results = []

    def chemical_reaction(self, promt: set) -> set[str]:
        if promt not in self.cache_reagents:
            equation = self.search(promt)
            self.cache_reagents.append(promt)
            self.cache_results.append(equation)


        return self.cache_results[self.cache_reagents.index(promt)]

    def search(self, promt: set) -> set[str] | None:
        req = requests.get(WEBSITE, {'s': '+'.join(promt)}).text
        equation = BeautifulSoup(req, 'html.parser').find('h1', {'class': 'equation main-equation well'})

        if equation is None: 
            print(None)
            return None

        elements = set()

        arrow = False
        if 'class="charge"' in str(equation):
            return None
        
        for span in equation.find_all('span', recursive=False):
            if span['class'] == ['arrow']: 
                arrow = True
            

            elif arrow and span['class'] == ['compound']:
                text = remove_trash(span.text)
                elements.add(text)
        if elements:
            print(f"reaction: {'+'.join(promt)} -> {'+'.join(elements)}")
            return elements 


if __name__ == '__main__':
    parcer = Chemistry()
    res = parcer.chemical_reaction({'kcl', 'h2o'})
    print(res)

