from links_getter import get_links
from Cocktail_info_getter import get_info

def main():
    links_list = get_links()
    print("Get links: Success")

    with open('./recipts.txt', 'w', encoding='utf-8') as file:
        i = 0
        for link in links_list:
            i += 1
            print(f'{i} of {len(links_list)}')
            try:
                info = get_info(link)
                if info[-1] != '':
                    file.write(str(info)+'\n')
                else:
                    print('No element')
            except ValueError:
                print('Error', i)
    


if __name__ == '__main__':
    main()