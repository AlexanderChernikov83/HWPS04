import wikipedia

def get_paragraphs(page):
    """Выводит список параграфов текущей статьи."""
    paragraphs = page.sections
    print("Параграфы статьи:")
    for i, section in enumerate(paragraphs, 1):
        print(f"{i}. {section}")
    return paragraphs

def show_links(page):
    """Выводит список связанных статей."""
    links = page.links[:10]  # Берем первые 10 ссылок для удобства
    print("Связанные статьи:")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")
    return links

def main():
    wikipedia.set_lang('ru')  # Устанавливаем язык Википедии (можно изменить на 'en' и др.)

    while True:
        # 1. Спрашиваем у пользователя первоначальный запрос
        query = input("\nВведите поисковый запрос для Википедии (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            print("До свидания!")
            break

        # 2. Ищем статью по запросу и переходим на неё
        try:
            results = wikipedia.search(query)
            if not results:
                print("Ничего не найдено. Попробуйте другой запрос.")
                continue

            page = wikipedia.page(results[0])  # Берём первую статью из результатов
            print(f"\nОткрыта статья: {page.title}")
            print(f"URL: {page.url}")

            while True:
                # 3. Предлагаем пользователю три варианта действий
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Выйти из программы")

                choice = input("Ваш выбор (1-3): ")

                if choice == '1':
                    # Листаем параграфы текущей статьи
                    sections = get_paragraphs(page)
                    if sections:
                        section_num = input("Введите номер параграфа для просмотра (или 'back' для возврата): ")
                        if section_num.lower() != 'back':
                            try:
                                section_idx = int(section_num) - 1
                                if 0 <= section_idx < len(sections):
                                    print(f"\n{sections[section_idx]}:")
                                    print(page.section(sections[section_idx]))
                                else:
                                    print("Неверный номер параграфа.")
                            except ValueError:
                                print("Пожалуйста, введите число.")

                elif choice == '2':
                    # Переходим на одну из связанных страниц
                    links = show_links(page)
                    link_num = input("Введите номер связанной статьи для перехода (или 'back' для возврата): ")
                    if link_num.lower() != 'back':
                        try:
                            link_idx = int(link_num) - 1
                            if 0 <= link_idx < len(links):
                                new_page = wikipedia.page(links[link_idx])
                                print(f"\nПерешли на статью: {new_page.title}")
                                print(f"URL: {new_page.url}")
                                page = new_page  # Обновляем текущую страницу
                            else:
                                print("Неверный номер статьи.")
                        except ValueError:
                            print("Пожалуйста, введите число.")
                        except wikipedia.DisambiguationError:
                            print("Ошибка: страница неоднозначна. Попробуйте другой выбор.")
                        except wikipedia.PageError:
                            print("Ошибка: страница не найдена. Попробуйте другой выбор.")

                elif choice == '3':
                    print("До свидания!")
                    return

                else:
                    print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

        except wikipedia.DisambiguationError as e:
            print(f"Ошибка: неоднозначный запрос. Попробуйте уточнить: {e}")
        except wikipedia.PageError:
            print("Ошибка: страница не найдена. Попробуйте другой запрос.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
