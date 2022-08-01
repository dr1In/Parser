import pymorphy2

nums = ['Sgtm sing', 'Pltm plur', 'sing']

morph = pymorphy2.MorphAnalyzer()

print(morph.parse('Ириски')[0].normal_form)